import os
from groq import Groq
import json
from backend.models.db import query_db

class SystemDesignTutor:
    """AI tutor for system design concepts"""
    
    def __init__(self):
        # Use Groq API
        self.client = Groq(
            api_key=os.environ.get("GROQ_API_KEY", "your-groq-api-key")
        )
        self.model = "llama3-70b-8192"  # Groq's Llama 3 model
        
        # Load System Design topic details
        self.load_topics()
        
    def load_topics(self):
        """Load system design topic details from the database or local file"""
        try:
            # Try to load from database - filter to only system design topics
            self.topics = query_db("SELECT * FROM topics WHERE category = 'system_design' ORDER BY order_num")
            if not self.topics:
                raise Exception("No system design topics found in database")
        except Exception:
            # Fall back to local file if database is not available
            data_path = os.path.join(os.path.dirname(__file__), '../../data/system_design_topics.json')
            with open(data_path, 'r') as f:
                self.topics = json.load(f)
    
    def get_topic_details(self, topic_id):
        """Get detailed information about a specific system design topic"""
        # First check if it's in our preloaded topics
        for topic in self.topics:
            if isinstance(topic, dict) and topic.get('id') == topic_id:
                return topic
            elif hasattr(topic, 'keys') and topic['id'] == topic_id:
                return dict(topic)
        
        # If not found, generate with the LLM
        prompt = f"""
        You are an expert system design instructor.
        Provide detailed information about the '{topic_id}' system design concept.
        Include the following:
        - Definition and overview
        - Key components or principles
        - Use cases and examples
        - Trade-offs and considerations
        - Best practices
        - Common mistakes or misconceptions
        
        Format your response as JSON with these fields: id, name, description, components, use_cases, trade_offs, best_practices, common_mistakes
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
        """Generate an explanation for a specific system design concept"""
        # Adjust the prompt based on the user's level
        level_prompts = {
            'beginner': "Explain in simple terms with basic examples. Avoid complex terminology.",
            'intermediate': "Include more detailed examples and some implementation considerations.",
            'advanced': "Provide in-depth analysis, including edge cases, scalability concerns, and optimization techniques."
        }
        
        level_guidance = level_prompts.get(level, level_prompts['beginner'])
        
        prompt = f"""
        You are an expert system design instructor helping a {level} level student.
        
        Explain the concept of '{concept}' in system design. {level_guidance}
        
        Format your response with:
        1. A clear definition
        2. Visual representation (using ASCII art if helpful)
        3. Key components or principles
        4. Real-world examples
        5. Implementation considerations
        6. Trade-offs and limitations
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": prompt}]
        )
        
        return response.choices[0].message.content
    
    def provide_case_study(self, topic_id, complexity='medium'):
        """Generate a case study for a specific system design topic"""
        # Define complexity levels
        complexity_guidance = {
            'simple': "Create a simple case study with minimal components and straightforward requirements.",
            'medium': "Create a moderately complex case study with multiple components and reasonable constraints.",
            'complex': "Create a complex case study with many interacting components, high scalability requirements, and various constraints."
        }
        
        # Use the appropriate complexity level
        guidance = complexity_guidance.get(complexity, complexity_guidance['medium'])
        
        prompt = f"""
        You are an expert system design instructor.
        
        Create a case study for the system design topic '{topic_id}'. {guidance}
        
        The case study should include:
        1. A realistic scenario or problem statement
        2. Specific requirements (functional and non-functional)
        3. Constraints and considerations
        4. Expected traffic/load/scale
        5. 2-3 key challenges to address
        
        Format your response to be engaging and educational, as if presenting this case study to students.
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": prompt}]
        )
        
        return response.choices[0].message.content
    
    def review_design(self, topic_id, design_description):
        """Review a user's system design and provide feedback"""
        prompt = f"""
        You are an expert system design instructor.
        
        A student has submitted a system design related to '{topic_id}'. Please review it and provide constructive feedback.
        
        Student's Design:
        ```
        {design_description}
        ```
        
        Provide feedback covering:
        1. Strengths of the design
        2. Areas for improvement
        3. Scalability considerations
        4. Reliability and fault tolerance
        5. Alternative approaches or trade-offs to consider
        
        Format your response as constructive feedback that helps the student improve their understanding and design skills.
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": prompt}]
        )
        
        return response.choices[0].message.content
    
    def generate_design_exercise(self, topic_id, difficulty='medium'):
        """Generate a system design exercise for a specific topic"""
        # Adjust difficulty
        difficulty_guidance = {
            'easy': "Create a straightforward exercise suitable for beginners.",
            'medium': "Create a moderately challenging exercise that requires understanding of multiple concepts.",
            'hard': "Create a complex exercise that mimics real-world system design interviews."
        }
        
        guidance = difficulty_guidance.get(difficulty, difficulty_guidance['medium'])
        
        prompt = f"""
        You are an expert system design instructor.
        
        Create a system design exercise related to '{topic_id}'. {guidance}
        
        The exercise should include:
        1. A clear problem statement and scenario
        2. Specific requirements and constraints
        3. Expected deliverables
        4. Evaluation criteria
        5. Hints or tips (without giving away the solution)
        
        Format the exercise as you would present it to students, with clear sections and engaging context.
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": prompt}]
        )
        
        return response.choices[0].message.content
    
    def provide_example_solution(self, exercise_id, detail_level='medium'):
        """Provide an example solution for a system design exercise"""
        # Adjust detail level
        detail_guidance = {
            'low': "Provide a high-level overview of the solution with key components.",
            'medium': "Provide a moderately detailed solution with components, interactions, and key considerations.",
            'high': "Provide a comprehensive solution with detailed components, interactions, trade-offs, and implementation notes."
        }
        
        guidance = detail_guidance.get(detail_level, detail_guidance['medium'])
        
        # Get exercise details (mock implementation)
        exercise = self._get_exercise(exercise_id)
        
        prompt = f"""
        You are an expert system design instructor.
        
        Provide an example solution for the following system design exercise. {guidance}
        
        Exercise: {exercise}
        
        Your solution should include:
        1. Architecture overview (with ASCII diagrams if helpful)
        2. Component breakdown
        3. Data flow description
        4. Scalability approach
        5. Handling edge cases and failures
        6. Technology choices with justification
        
        Format your response to be educational, explaining your reasoning for design choices.
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": prompt}]
        )
        
        return response.choices[0].message.content
    
    def _get_exercise(self, exercise_id):
        """Get exercise details by ID (mock implementation)"""
        # In a real implementation, this would fetch from the database
        exercises = {
            "load_balancing_1": "Design a load balancing system for a high-traffic web application with 10M daily active users.",
            "database_scaling_1": "Design a database architecture that can handle 5000 writes/second and 50000 reads/second for an e-commerce platform.",
            "microservices_1": "Design a microservices architecture for a food delivery application.",
            "default": "Design a scalable and reliable system that meets the specified requirements."
        }
        
        return exercises.get(exercise_id, exercises["default"])