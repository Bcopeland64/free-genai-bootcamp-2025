import os
from groq import Groq
import json
from backend.models.db import query_db

class DSATutor:
    """AI tutor for data structures and algorithms"""
    
    def __init__(self):
        # Use Groq API instead of OpenAI/Ollama
        self.client = Groq(
            api_key=os.environ.get("GROQ_API_KEY", "your-groq-api-key")  # Get from environment or set a default
        )
        self.model = "llama3-70b-8192"  # Groq's Llama 3 model
        
        # Load DSA topic details
        self.load_topics()
        
    def load_topics(self):
        """Load DSA topic details from the database or local file"""
        try:
            # Try to load from database - filter to only DSA topics
            self.topics = query_db("SELECT * FROM topics WHERE category = 'dsa' ORDER BY order_num")
            if not self.topics:
                raise Exception("No DSA topics found in database")
        except Exception:
            # Fall back to local file if database is not available
            data_path = os.path.join(os.path.dirname(__file__), '../../data/dsa_topics.json')
            with open(data_path, 'r') as f:
                self.topics = json.load(f)
    
    def get_topic_details(self, topic_id):
        """Get detailed information about a specific DSA topic"""
        # First check if it's in our preloaded topics
        for topic in self.topics:
            if isinstance(topic, dict) and topic.get('id') == topic_id:
                return topic
            elif hasattr(topic, 'keys') and topic['id'] == topic_id:
                return dict(topic)
        
        # If not found, generate with the LLM
        prompt = f"""
        You are an expert data structures and algorithms tutor.
        Provide detailed information about the '{topic_id}' data structure or algorithm.
        Include the following:
        - Definition and overview
        - Time and space complexity for key operations
        - Common use cases
        - Implementation considerations in Python
        - Common pitfalls or misconceptions
        
        Format your response as JSON with these fields: id, name, description, time_complexity, space_complexity, use_cases, implementation_notes, common_pitfalls
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
        """Generate an explanation for a specific DSA concept"""
        # Adjust the prompt based on the user's level
        level_prompts = {
            'beginner': "Explain in simple terms with basic examples. Avoid complex terminology.",
            'intermediate': "Include more detailed examples and some implementation considerations.",
            'advanced': "Provide in-depth analysis, including edge cases and optimization techniques."
        }
        
        level_guidance = level_prompts.get(level, level_prompts['beginner'])
        
        prompt = f"""
        You are an expert data structures and algorithms tutor helping a {level} level student.
        
        Explain the concept of '{concept}' in Python. {level_guidance}
        
        Format your response with:
        1. A clear definition
        2. Visual representation (using ASCII art if helpful)
        3. Python code examples
        4. Time and space complexity analysis
        5. Common use cases
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": prompt}]
        )
        
        return response.choices[0].message.content
    
    def provide_walkthrough(self, problem_id, hint_level=0):
        """Generate a step-by-step walkthrough for a specific problem"""
        # Get problem details from database
        problem = query_db("SELECT * FROM problems WHERE id = ?", [problem_id], one=True)
        
        if not problem:
            return "Problem not found. Please check the problem ID and try again."
        
        # Define hint levels
        hint_guidance = [
            "Give a high-level approach without specific code solutions. Focus on problem understanding and conceptual steps.",
            "Provide more specific algorithmic hints and pseudocode, but still let the student implement details.",
            "Offer a complete walkthrough with Python code snippets for each step, explaining why each step is necessary."
        ]
        
        # Use the appropriate hint level (default to 0 if out of range)
        hint_level = min(max(0, hint_level), len(hint_guidance) - 1)
        
        prompt = f"""
        You are an expert data structures and algorithms tutor.
        
        Problem: {problem['description'] if hasattr(problem, 'description') else problem.get('description')}
        
        Provide a walkthrough for this problem. {hint_guidance[hint_level]}
        
        Format your response with:
        1. Problem understanding
        2. Breaking down the problem
        3. Approach selection with reasoning
        4. Step-by-step solution development
        5. Complexity analysis
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": prompt}]
        )
        
        return response.choices[0].message.content
    
    def generate_practice_problems(self, topic_id, difficulty='easy'):
        """Generate practice problems for a specific topic"""
        prompt = f"""
        You are an expert data structures and algorithms tutor.
        
        Create 3 {difficulty} practice problems for the topic '{topic_id}'.
        
        For each problem, include:
        1. A clear problem statement
        2. Example input and expected output
        3. Constraints and assumptions
        4. A hint for approaching the problem
        
        Format your response as a JSON array with these fields for each problem: id, title, description, examples, constraints, hint
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
    
    def review_code_solution(self, problem_id, code):
        """Review a user's code solution and provide feedback"""
        # Get problem details
        problem = query_db("SELECT * FROM problems WHERE id = ?", [problem_id], one=True)
        
        if not problem:
            return {"error": "Problem not found"}
        
        prompt = f"""
        You are an expert data structures and algorithms tutor.
        
        Problem: {problem['description'] if hasattr(problem, 'description') else problem.get('description')}
        
        User's Python solution:
        ```python
        {code}
        ```
        
        Provide a detailed code review covering:
        1. Correctness - Does the solution work for all cases?
        2. Time complexity analysis
        3. Space complexity analysis
        4. Code style and Pythonic improvements
        5. Edge cases consideration
        6. Alternative approaches
        
        Format your response as constructive feedback a teacher would give to a student.
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": prompt}]
        )
        
        return response.choices[0].message.content