from flask import Blueprint, request, jsonify
import sys
import os

# Update path to include agents from project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from agents.tutors.dsa_tutor import DSATutor
from agents.tutors.system_design_tutor import SystemDesignTutor
from agents.tutors.math_tutor import MathTutor
from agents.evaluators.code_evaluator import CodeEvaluator
from backend.models.progress import UserProgress
from backend.models.db import query_db
import json
import os

# Create blueprints for different API sections
topics_bp = Blueprint('topics', __name__, url_prefix='/api/topics')
dsa_bp = Blueprint('dsa', __name__, url_prefix='/api/dsa')
system_design_bp = Blueprint('system_design', __name__, url_prefix='/api/system_design')
math_bp = Blueprint('math', __name__, url_prefix='/api/math')
tutor_bp = Blueprint('tutor', __name__, url_prefix='/api/tutor')
exercise_bp = Blueprint('exercise', __name__, url_prefix='/api/exercise')
progress_bp = Blueprint('progress', __name__, url_prefix='/api/progress')

# Topic routes
@topics_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all available topic categories"""
    categories = [
        {"id": "dsa", "name": "Data Structures & Algorithms", "description": "Learn essential data structures and algorithms for technical interviews and efficient programming."},
        {"id": "system_design", "name": "System Design", "description": "Master design principles for large-scale systems, including scalability, reliability, and performance."},
        {"id": "math", "name": "Mathematics", "description": "Study key mathematical concepts including calculus, linear algebra, and statistics for technical applications."}
    ]
    return jsonify(categories)

@topics_bp.route('/<category>', methods=['GET'])
def get_topics_by_category(category):
    """Get all topics for a specific category"""
    try:
        # Try to load from database
        topics = query_db("SELECT * FROM topics WHERE category = ? ORDER BY order_num", [category])
        
        if not topics:
            raise Exception("No topics found in database")
        
        # Convert row objects to dicts
        topic_list = [dict(topic) for topic in topics]
        return jsonify(topic_list)
    
    except Exception as e:
        # Fall back to local file if database is not available
        try:
            data_path = os.path.join(os.path.dirname(__file__), f'../../data/{category}_topics.json')
            with open(data_path, 'r') as f:
                topics = json.load(f)
            return jsonify(topics)
        except:
            # Return empty list if no file exists
            return jsonify([])

# DSA routes
@dsa_bp.route('/topics', methods=['GET'])
def get_dsa_topics():
    """Get all available DSA topics"""
    try:
        # Try to load from database
        topics = query_db("SELECT id, name, level, subcategory, order_num FROM topics WHERE category = 'dsa' ORDER BY order_num")
        
        if not topics:
            raise Exception("No topics found in database")
        
        # Convert row objects to dicts
        topic_list = [dict(topic) for topic in topics]
        return jsonify(topic_list)
    
    except Exception:
        # Fall back to local file if database is not available
        data_path = os.path.join(os.path.dirname(__file__), '../../data/dsa_topics.json')
        with open(data_path, 'r') as f:
            topics = json.load(f)
            # Extract only the required fields
            simplified_topics = [{"id": t["id"], "name": t["name"], "level": t["level"], 
                                 "subcategory": t.get("subcategory"), "order_num": t["order_num"]} 
                                for t in topics]
        return jsonify(simplified_topics)

@dsa_bp.route('/topics/<topic_id>', methods=['GET'])
def get_dsa_topic_details(topic_id):
    """Get detailed information about a specific DSA topic"""
    tutor = DSATutor()
    topic_details = tutor.get_topic_details(topic_id)
    return jsonify(topic_details)

# System Design routes
@system_design_bp.route('/topics', methods=['GET'])
def get_system_design_topics():
    """Get all available system design topics"""
    try:
        topics = query_db("SELECT id, name, level, subcategory, order_num FROM topics WHERE category = 'system_design' ORDER BY order_num")
        
        if not topics:
            raise Exception("No topics found in database")
        
        topic_list = [dict(topic) for topic in topics]
        return jsonify(topic_list)
    
    except Exception:
        data_path = os.path.join(os.path.dirname(__file__), '../../data/system_design_topics.json')
        with open(data_path, 'r') as f:
            topics = json.load(f)
            simplified_topics = [{"id": t["id"], "name": t["name"], "level": t["level"], 
                                 "subcategory": t.get("subcategory"), "order_num": t["order_num"]} 
                                for t in topics]
        return jsonify(simplified_topics)

@system_design_bp.route('/topics/<topic_id>', methods=['GET'])
def get_system_design_topic_details(topic_id):
    """Get detailed information about a specific system design topic"""
    tutor = SystemDesignTutor()
    topic_details = tutor.get_topic_details(topic_id)
    return jsonify(topic_details)

@system_design_bp.route('/case_study/<topic_id>', methods=['GET'])
def get_case_study(topic_id):
    """Get a case study for a specific system design topic"""
    complexity = request.args.get('complexity', 'medium')
    
    tutor = SystemDesignTutor()
    case_study = tutor.provide_case_study(topic_id, complexity)
    return jsonify({"case_study": case_study})

@system_design_bp.route('/exercise/<topic_id>', methods=['GET'])
def get_design_exercise(topic_id):
    """Get a system design exercise for a specific topic"""
    difficulty = request.args.get('difficulty', 'medium')
    
    tutor = SystemDesignTutor()
    exercise = tutor.generate_design_exercise(topic_id, difficulty)
    return jsonify({"exercise": exercise})

@system_design_bp.route('/review', methods=['POST'])
def review_design():
    """Review a user's system design solution"""
    data = request.json
    topic_id = data.get('topic_id', '')
    design = data.get('design', '')
    
    try:
        tutor = SystemDesignTutor()
        review = tutor.review_design(topic_id, design)
        return jsonify({"review": review})
    except Exception as e:
        print(f"Error in review_design: {str(e)}")
        return jsonify({"review": f"We encountered an error when analyzing your design. Error: {str(e)}", 
                        "error": str(e)})

# Math routes
@math_bp.route('/topics', methods=['GET'])
def get_math_topics():
    """Get all available math topics"""
    subcategory = request.args.get('subcategory', None)
    
    try:
        if subcategory:
            topics = query_db("SELECT id, name, level, subcategory, order_num FROM topics WHERE category = 'math' AND subcategory = ? ORDER BY order_num", [subcategory])
        else:
            topics = query_db("SELECT id, name, level, subcategory, order_num FROM topics WHERE category = 'math' ORDER BY order_num")
        
        if not topics:
            raise Exception("No topics found in database")
        
        topic_list = [dict(topic) for topic in topics]
        return jsonify(topic_list)
    
    except Exception:
        data_path = os.path.join(os.path.dirname(__file__), '../../data/math_topics.json')
        with open(data_path, 'r') as f:
            topics = json.load(f)
            
            # Filter by subcategory if specified
            if subcategory:
                topics = [t for t in topics if t.get("subcategory") == subcategory]
                
            simplified_topics = [{"id": t["id"], "name": t["name"], "level": t["level"], 
                                 "subcategory": t.get("subcategory"), "order_num": t["order_num"]} 
                                for t in topics]
        return jsonify(simplified_topics)

@math_bp.route('/topics/<topic_id>', methods=['GET'])
def get_math_topic_details(topic_id):
    """Get detailed information about a specific math topic"""
    tutor = MathTutor()
    topic_details = tutor.get_topic_details(topic_id)
    return jsonify(topic_details)

@math_bp.route('/problems/<topic_id>', methods=['GET'])
def get_math_problems(topic_id):
    """Get math problems for a specific topic"""
    difficulty = request.args.get('difficulty', 'all')
    
    try:
        if difficulty != 'all':
            problems = query_db(
                "SELECT * FROM math_problems WHERE topic_id = ? AND difficulty = ? ORDER BY id", 
                [topic_id, difficulty]
            )
        else:
            problems = query_db(
                "SELECT * FROM math_problems WHERE topic_id = ? ORDER BY id", 
                [topic_id]
            )
        
        if not problems:
            raise Exception("No problems found in database")
        
        problem_list = [dict(problem) for problem in problems]
        return jsonify(problem_list)
    
    except Exception:
        # Fall back to local file
        try:
            data_path = os.path.join(os.path.dirname(__file__), '../../data/math_problems.json')
            with open(data_path, 'r') as f:
                all_problems = json.load(f)
                
            # Filter problems by topic and difficulty
            problems = [p for p in all_problems if p["topic_id"] == topic_id]
            if difficulty != 'all':
                problems = [p for p in problems if p["difficulty"] == difficulty]
                
            return jsonify(problems)
        except:
            return jsonify([])

@math_bp.route('/solve', methods=['POST'])
def solve_math_problem():
    """Solve a math problem with step-by-step explanation"""
    data = request.json
    problem = data.get('problem')
    show_steps = data.get('show_steps', True)
    
    tutor = MathTutor()
    solution = tutor.solve_problem(problem, show_steps)
    return jsonify({"solution": solution})

@math_bp.route('/check', methods=['POST'])
def check_math_solution():
    """Check a student's solution to a math problem"""
    data = request.json
    problem = data.get('problem')
    solution = data.get('solution')
    
    tutor = MathTutor()
    feedback = tutor.check_solution(problem, solution)
    return jsonify({"feedback": feedback})

# Tutor routes
@tutor_bp.route('/explain', methods=['POST'])
def explain_concept():
    """Get an explanation for a specific concept"""
    data = request.json
    concept = data.get('concept')
    level = data.get('level', 'beginner')
    category = data.get('category', 'dsa')
    
    if category == 'dsa':
        tutor = DSATutor()
    elif category == 'system_design':
        tutor = SystemDesignTutor()
    elif category == 'math':
        tutor = MathTutor()
    else:
        return jsonify({"error": "Invalid category"}), 400
    
    explanation = tutor.explain_concept(concept, level)
    return jsonify({"explanation": explanation})

@tutor_bp.route('/walkthrough', methods=['POST'])
def solution_walkthrough():
    """Get a step-by-step walkthrough for a specific problem"""
    data = request.json
    problem_id = data.get('problem_id')
    hint_level = data.get('hint_level', 0)
    category = data.get('category', 'dsa')
    
    if category == 'dsa':
        tutor = DSATutor()
        walkthrough = tutor.provide_walkthrough(problem_id, hint_level)
    else:
        return jsonify({"error": "Walkthrough not supported for this category"}), 400
    
    return jsonify({"walkthrough": walkthrough})

# Exercise routes
@exercise_bp.route('/problems/<topic_id>', methods=['GET'])
def get_topic_problems(topic_id):
    """Get practice problems for a specific topic"""
    difficulty = request.args.get('difficulty', 'easy')
    category = request.args.get('category', 'dsa')
    
    # Redirect to appropriate route based on category
    if category == 'math':
        return get_math_problems(topic_id)
    
    try:
        if difficulty != 'all':
            problems = query_db(
                "SELECT * FROM problems WHERE topic_id = ? AND difficulty = ? ORDER BY id", 
                [topic_id, difficulty]
            )
        else:
            problems = query_db(
                "SELECT * FROM problems WHERE topic_id = ? ORDER BY id", 
                [topic_id]
            )
        
        if not problems:
            raise Exception("No problems found in database")
        
        problem_list = [dict(problem) for problem in problems]
        return jsonify(problem_list)
    
    except Exception:
        # Fallback mock data
        problems = [
            {"id": f"{topic_id}_1", "title": "Problem 1", "difficulty": "easy"},
            {"id": f"{topic_id}_2", "title": "Problem 2", "difficulty": "medium"},
            {"id": f"{topic_id}_3", "title": "Problem 3", "difficulty": "hard"}
        ]
        
        # Filter by difficulty if specified
        if difficulty != 'all':
            problems = [p for p in problems if p['difficulty'] == difficulty]
            
        return jsonify(problems)

@exercise_bp.route('/evaluate', methods=['POST'])
def evaluate_solution():
    """Evaluate a user's solution to a problem"""
    data = request.json
    problem_id = data.get('problem_id')
    code = data.get('code')
    language = data.get('language', 'python')
    
    evaluator = CodeEvaluator()
    result = evaluator.evaluate(problem_id, code, language)
    return jsonify(result)

# Progress routes
@progress_bp.route('/user/<user_id>', methods=['GET'])
def get_user_progress(user_id):
    """Get a user's learning progress"""
    category = request.args.get('category', 'all')
    
    progress = UserProgress.get_progress(user_id, category)
    return jsonify(progress)

@progress_bp.route('/update', methods=['POST'])
def update_progress():
    """Update a user's learning progress"""
    data = request.json
    user_id = data.get('user_id')
    topic_id = data.get('topic_id')
    item_id = data.get('item_id')
    item_type = data.get('item_type', 'problem')
    completed = data.get('completed', False)
    
    success = UserProgress.update_progress(user_id, topic_id, item_id, item_type, completed)
    return jsonify({"success": success})

@progress_bp.route('/recommendations/<user_id>', methods=['GET'])
def get_recommendations(user_id):
    """Get recommended topics for a user based on their progress"""
    category = request.args.get('category', 'all')
    
    recommendations = UserProgress.get_recommended_topics(user_id, category)
    return jsonify(recommendations)

# Learning path routes
@topics_bp.route('/learning_paths', methods=['GET'])
def get_learning_paths():
    """Get all available learning paths"""
    category = request.args.get('category', 'all')
    
    try:
        if category != 'all':
            paths = query_db(
                "SELECT * FROM learning_paths WHERE category = ? ORDER BY id", 
                [category]
            )
        else:
            paths = query_db("SELECT * FROM learning_paths ORDER BY id")
        
        if not paths:
            raise Exception("No learning paths found in database")
        
        path_list = [dict(path) for path in paths]
        return jsonify(path_list)
    
    except Exception:
        # Fallback mock data
        paths = [
            {"id": 1, "name": "DSA Fundamentals", "description": "Learn the essential data structures and algorithms", "category": "dsa", "difficulty": "beginner"},
            {"id": 2, "name": "System Design Basics", "description": "Understand core concepts of system design", "category": "system_design", "difficulty": "beginner"},
            {"id": 3, "name": "Applied Mathematics", "description": "Master key mathematical concepts for computer science", "category": "math", "difficulty": "intermediate"}
        ]
        
        # Filter by category if specified
        if category != 'all':
            paths = [p for p in paths if p['category'] == category]
            
        return jsonify(paths)

@topics_bp.route('/learning_paths/<path_id>', methods=['GET'])
def get_learning_path_details(path_id):
    """Get details of a specific learning path, including its topics"""
    try:
        path = query_db("SELECT * FROM learning_paths WHERE id = ?", [path_id], one=True)
        
        if not path:
            raise Exception("Learning path not found")
        
        # Get the topics in this learning path
        path_topics = query_db(
            """
            SELECT t.* FROM topics t
            JOIN learning_path_topics lpt ON t.id = lpt.topic_id
            WHERE lpt.learning_path_id = ?
            ORDER BY lpt.order_num
            """,
            [path_id]
        )
        
        path_dict = dict(path)
        path_dict['topics'] = [dict(topic) for topic in path_topics]
        
        return jsonify(path_dict)
    
    except Exception as e:
        # Fallback mock data for a specific path
        if path_id == '1':  # DSA Fundamentals
            return jsonify({
                "id": 1,
                "name": "DSA Fundamentals",
                "description": "Learn the essential data structures and algorithms",
                "category": "dsa",
                "difficulty": "beginner",
                "topics": [
                    {"id": "arrays", "name": "Arrays", "level": "beginner"},
                    {"id": "linked_lists", "name": "Linked Lists", "level": "beginner"},
                    {"id": "stacks", "name": "Stacks", "level": "beginner"},
                    {"id": "queues", "name": "Queues", "level": "beginner"}
                ]
            })
        else:
            return jsonify({"error": "Learning path not found"}), 404

def register_routes(app):
    """Register all blueprints with the Flask app"""
    app.register_blueprint(topics_bp)
    app.register_blueprint(dsa_bp)
    app.register_blueprint(system_design_bp)
    app.register_blueprint(math_bp)
    app.register_blueprint(tutor_bp)
    app.register_blueprint(exercise_bp)
    app.register_blueprint(progress_bp)