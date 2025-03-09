import os
from groq import Groq
import json
import re
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from backend.models.db import query_db

class MathTutor:
    """AI tutor for mathematics concepts including calculus, linear algebra, and statistics"""
    
    def __init__(self):
        # Use Groq API
        self.client = Groq(
            api_key=os.environ.get("GROQ_API_KEY", "your-groq-api-key")
        )
        self.model = "llama3-70b-8192"  # Groq's Llama 3 model
        
        # Load Math topic details
        self.load_topics()
        
    def load_topics(self):
        """Load math topic details from the database or local file"""
        try:
            # Try to load from database - filter to only math topics
            self.topics = query_db("SELECT * FROM topics WHERE category = 'math' ORDER BY order_num")
            if not self.topics:
                raise Exception("No math topics found in database")
        except Exception:
            # Fall back to local file if database is not available
            data_path = os.path.join(os.path.dirname(__file__), '../../data/math_topics.json')
            with open(data_path, 'r') as f:
                self.topics = json.load(f)
    
    def get_topic_details(self, topic_id):
        """Get detailed information about a specific math topic"""
        # First check if it's in our preloaded topics
        for topic in self.topics:
            if isinstance(topic, dict) and topic.get('id') == topic_id:
                return topic
            elif hasattr(topic, 'keys') and topic['id'] == topic_id:
                return dict(topic)
        
        # If not found, generate with the LLM
        prompt = f"""
        You are an expert mathematics tutor.
        Provide detailed information about the '{topic_id}' math concept.
        Include the following:
        - Definition and overview
        - Key formulas and properties
        - Applications and use cases
        - Common misconceptions
        - Related concepts
        
        Format your response as JSON with these fields: id, name, description, key_formulas, applications, misconceptions, related_concepts
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        # Parse and return the JSON response
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            # Fallback if response is not valid JSON
            return {
                "id": topic_id,
                "name": topic_id.replace('_', ' ').title(),
                "description": "Information about this topic is currently being updated.",
                "level": "beginner"
            }
    
    def explain_concept(self, concept, level='beginner'):
        """Generate an explanation for a specific math concept"""
        # Adjust the prompt based on the user's level
        level_prompts = {
            'beginner': "Explain in simple terms with basic examples. Use intuitive visualizations and avoid complex notation.",
            'intermediate': "Include more rigorous definitions and examples, with some proofs or derivations where helpful.",
            'advanced': "Provide a comprehensive explanation with formal definitions, theorems, proofs, and advanced applications."
        }
        
        level_guidance = level_prompts.get(level, level_prompts['beginner'])
        
        prompt = f"""
        You are an expert mathematics tutor helping a {level} level student.
        
        Explain the concept of '{concept}' in mathematics. {level_guidance}
        
        Format your response with:
        1. A clear definition
        2. Intuitive explanation (with analogies if helpful)
        3. Key formulas or properties
        4. Step-by-step examples
        5. Applications
        
        Use LaTeX for mathematical notation enclosed in dollar signs (e.g., $f(x) = x^2$).
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": prompt}]
        )
        
        # Process the response to handle LaTeX formatting for Streamlit
        content = response.choices[0].message.content
        # Note: In the actual implementation, we'd render LaTeX using Streamlit's support for it
        
        return content
    
    def solve_problem(self, problem, show_steps=True):
        """Solve a mathematical problem with step-by-step explanation"""
        # Determine the type of problem (calculus, linear algebra, statistics)
        problem_type = self._determine_problem_type(problem)
        
        step_guidance = "Provide a detailed step-by-step solution, explaining your reasoning at each step." if show_steps else "Provide just the final answer with minimal explanation."
        
        prompt = f"""
        You are an expert mathematics tutor specializing in {problem_type}.
        
        Solve the following problem: {problem}
        
        {step_guidance}
        
        Format your response with:
        1. Problem restatement
        2. Approach overview
        3. Step-by-step solution (if requested)
        4. Final answer clearly marked
        
        Use LaTeX for mathematical notation enclosed in dollar signs (e.g., $f(x) = x^2$).
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": prompt}]
        )
        
        return response.choices[0].message.content
    
    def _determine_problem_type(self, problem):
        """Determine the type of math problem based on its content"""
        # Check for calculus-related terms
        calculus_terms = ['derivative', 'integral', 'limit', 'differentiate', 'integrate', 
                         'dx', 'dy', 'maximum', 'minimum', 'extrema']
        
        # Check for linear algebra terms
        linear_algebra_terms = ['matrix', 'vector', 'eigenvalue', 'eigenvector', 'linear transformation',
                              'determinant', 'orthogonal', 'span', 'basis', 'rank']
        
        # Check for statistics terms
        statistics_terms = ['probability', 'distribution', 'mean', 'variance', 'standard deviation',
                          'hypothesis test', 'p-value', 'confidence interval', 'regression', 'correlation']
        
        # Count occurrences of each type of term
        calculus_count = sum(1 for term in calculus_terms if term.lower() in problem.lower())
        linear_algebra_count = sum(1 for term in linear_algebra_terms if term.lower() in problem.lower())
        statistics_count = sum(1 for term in statistics_terms if term.lower() in problem.lower())
        
        # Determine the most likely type
        if calculus_count >= linear_algebra_count and calculus_count >= statistics_count:
            return "calculus"
        elif linear_algebra_count >= calculus_count and linear_algebra_count >= statistics_count:
            return "linear algebra"
        elif statistics_count >= calculus_count and statistics_count >= linear_algebra_count:
            return "statistics"
        else:
            return "mathematics"  # Generic fallback
    
    def generate_practice_problems(self, topic_id, difficulty='medium', count=3):
        """Generate practice problems for a specific math topic"""
        # Adjust difficulty
        difficulty_guidance = {
            'easy': "Create straightforward problems that test basic understanding and application.",
            'medium': "Create moderately challenging problems that require deeper understanding and multiple steps.",
            'hard': "Create complex problems that require synthesis of multiple concepts and creative problem-solving."
        }
        
        guidance = difficulty_guidance.get(difficulty, difficulty_guidance['medium'])
        
        prompt = f"""
        You are an expert mathematics tutor.
        
        Create {count} {difficulty} practice problems for the math topic '{topic_id}'.
        
        {guidance}
        
        For each problem, include:
        1. A clear problem statement
        2. Any necessary context or setup
        3. The answer (separated clearly so it can be hidden from students initially)
        
        Format your response as a JSON array with these fields for each problem: id, problem, answer, difficulty
        Use LaTeX for mathematical notation enclosed in double dollar signs (e.g., $$f(x) = x^2$$).
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return {"error": "Failed to generate problems. Please try again."}
    
    def check_solution(self, problem, student_solution):
        """Check a student's solution to a math problem and provide feedback"""
        prompt = f"""
        You are an expert mathematics tutor.
        
        Problem: {problem}
        
        Student's solution:
        ```
        {student_solution}
        ```
        
        Carefully analyze the student's solution and provide feedback:
        1. Is the final answer correct? If not, what is the correct answer?
        2. Are there any errors in the steps or reasoning? If so, identify them specifically.
        3. Are there any more elegant or efficient approaches?
        4. What concepts does the student seem to understand well?
        5. What concepts might the student need to review?
        
        Format your response to be constructive and educational, focusing on helping the student improve their understanding.
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": prompt}]
        )
        
        return response.choices[0].message.content
    
    def generate_visualization(self, concept, data=None):
        """Generate a visualization for a mathematical concept or dataset"""
        # This is a simplified implementation that would need to be expanded
        # In a real application, we would use matplotlib, plotly, or other visualization libraries
        
        # Example: generate a simple plot for a function
        if concept.startswith("function:"):
            function_str = concept.replace("function:", "").strip()
            return self._visualize_function(function_str)
        
        # Example: generate a statistical visualization from data
        elif concept == "statistics" and data is not None:
            return self._visualize_statistics(data)
        
        # For other concepts, generate a text description of what the visualization would show
        else:
            prompt = f"""
            You are an expert mathematics tutor.
            
            Describe how you would visualize the concept of '{concept}' to help a student understand it.
            Include details about:
            1. What type of visualization would be most helpful (graph, diagram, etc.)
            2. What specific elements would be included
            3. How the visualization connects to the key aspects of the concept
            
            Focus on making the visualization intuitive and educational.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": prompt}]
            )
            
            return response.choices[0].message.content
    
    def _visualize_function(self, function_str):
        """Create a visualization of a mathematical function"""
        # This would be implemented with matplotlib in the actual application
        # For now, return a description
        return f"Visualization of function {function_str} would be created using matplotlib."
    
    def _visualize_statistics(self, data):
        """Create a statistical visualization from data"""
        # This would be implemented with matplotlib or seaborn in the actual application
        # For now, return a description
        return f"Statistical visualization of the provided data would be created using matplotlib or seaborn."
    
    def generate_learning_path(self, topic_id, current_level='beginner', target_level='advanced'):
        """Generate a customized learning path for a specific math topic"""
        prompt = f"""
        You are an expert mathematics tutor.
        
        Create a structured learning path for a student to progress from {current_level} to {target_level} level in the topic of '{topic_id}'.
        
        The learning path should include:
        1. Prerequisites that should be mastered first
        2. A sequence of concepts to learn, in order
        3. Recommended resources for each concept (textbooks, online courses, videos)
        4. Practice milestones that indicate mastery at each stage
        5. Estimated time commitment for each stage
        
        Format your response as a clear, structured learning roadmap that a student could follow.
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": prompt}]
        )
        
        return response.choices[0].message.content