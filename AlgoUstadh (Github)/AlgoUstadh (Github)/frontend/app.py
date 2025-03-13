import streamlit as st
import requests
import json
import os
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import io
import base64
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from streamlit_extras.colored_header import colored_header
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.grid import grid

# Setup API URL (change when deploying)
API_URL = "http://localhost:5000/api"

# App title and configuration
st.set_page_config(
    page_title="Algo Ustadh - Learn CS Fundamentals",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for app
if "user_id" not in st.session_state:
    st.session_state.user_id = "demo_user"  # For demo purposes
if "current_topic" not in st.session_state:
    st.session_state.current_topic = None
if "current_problem" not in st.session_state:
    st.session_state.current_problem = None
if "current_category" not in st.session_state:
    st.session_state.current_category = "dsa"  # Default category
if "code_solution" not in st.session_state:
    st.session_state.code_solution = ""
if "design_solution" not in st.session_state:
    st.session_state.design_solution = ""
if "math_solution" not in st.session_state:
    st.session_state.math_solution = ""
if "evaluation_result" not in st.session_state:
    st.session_state.evaluation_result = None
if "hint_level" not in st.session_state:
    st.session_state.hint_level = 0

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #1E3A8A;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        letter-spacing: -0.5px;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        color: #374151;
    }
    .category-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #334155;
    }
    .topic-card {
        padding: 1.5rem;
        border-radius: 0.7rem;
        background-color: #f8fafc;
        margin-bottom: 1rem;
        border-left: 5px solid #3B82F6;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
    }
    .topic-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    .topic-title {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        color: #1F2937;
    }
    .topic-desc {
        color: #4B5563;
        margin-bottom: 0.5rem;
        font-size: 0.95rem;
    }
    .concept-header {
        font-size: 1.5rem;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
        border-bottom: 2px solid #3B82F6;
        padding-bottom: 0.5rem;
        color: #1F2937;
    }
    .content-section {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.7rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
    .code-editor {
        border-radius: 0.5rem;
        border: 1px solid #E5E7EB;
        margin-top: 1rem;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
    }
    .hint-box {
        background-color: #EFF6FF;
        border-left: 5px solid #3B82F6;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.375rem;
    }
    .success-box {
        background-color: #ECFDF5;
        border-left: 5px solid #10B981;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.375rem;
    }
    .error-box {
        background-color: #FEF2F2;
        border-left: 5px solid #EF4444;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.375rem;
    }
    .info-box {
        background-color: #F3F4F6;
        border-left: 5px solid #6B7280;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.375rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        border-radius: 4px 4px 0 0;
        gap: 1;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #EFF6FF;
        border-bottom-color: #3B82F6;
        font-weight: bold;
    }
    .category-selector {
        padding: 10px 15px;
        margin-bottom: 20px;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.2s ease;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .category-selector:hover {
        background-color: #EFF6FF;
    }
    .category-selector.active {
        background-color: #DBEAFE;
        color: #1E40AF;
    }
    .sidebar-title {
        font-size: 1.2rem;
        font-weight: bold;
        margin: 1rem 0;
        color: #1F2937;
    }
    /* Emoji badges for difficulty levels */
    .badge-beginner {
        background-color: #DCFCE7;
        color: #166534;
        padding: 3px 8px;
        border-radius: 10px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .badge-intermediate {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 3px 8px;
        border-radius: 10px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .badge-advanced {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 3px 8px;
        border-radius: 10px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    /* Math formatting */
    .katex-display {
        overflow: auto hidden;
        font-size: 1.2rem;
    }
    /* Code snippets */
    pre {
        background-color: #F9FAFB;
        border-radius: 0.5rem;
        padding: 1rem;
        overflow-x: auto;
        margin: 1rem 0;
        border: 1px solid #E5E7EB;
    }
    code {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem;
        color: #1F2937;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions for API calls
def get_categories():
    """Get all available categories"""
    try:
        response = requests.get(f"{API_URL}/topics/categories")
        return response.json()
    except Exception as e:
        # Fallback if API is not available
        return [
            {"id": "dsa", "name": "Data Structures & Algorithms", "description": "Learn essential data structures and algorithms for technical interviews and efficient programming."},
            {"id": "system_design", "name": "System Design", "description": "Master design principles for large-scale systems, including scalability, reliability, and performance."},
            {"id": "math", "name": "Mathematics", "description": "Study key mathematical concepts including calculus, linear algebra, and statistics for technical applications."}
        ]

def get_topics(category="dsa"):
    """Get topics for a specific category"""
    try:
        if category == "dsa":
            response = requests.get(f"{API_URL}/dsa/topics")
        elif category == "system_design":
            response = requests.get(f"{API_URL}/system_design/topics")
        elif category == "math":
            response = requests.get(f"{API_URL}/math/topics")
        else:
            response = requests.get(f"{API_URL}/topics/{category}")
        
        return response.json()
    except Exception as e:
        # Fallback data based on category
        if category == "dsa":
            return [
                {"id": "arrays", "name": "Arrays", "level": "beginner"},
                {"id": "linked_lists", "name": "Linked Lists", "level": "beginner"},
                {"id": "stacks", "name": "Stacks", "level": "beginner"},
                {"id": "queues", "name": "Queues", "level": "beginner"},
                {"id": "hash_tables", "name": "Hash Tables", "level": "intermediate"},
                {"id": "trees", "name": "Trees", "level": "intermediate"},
                {"id": "sorting", "name": "Sorting Algorithms", "level": "intermediate"},
                {"id": "dynamic_programming", "name": "Dynamic Programming", "level": "advanced"}
            ]
        elif category == "system_design":
            return [
                {"id": "system_design_fundamentals", "name": "System Design Fundamentals", "level": "beginner"},
                {"id": "scalability", "name": "Scalability", "level": "beginner"},
                {"id": "load_balancing", "name": "Load Balancing", "level": "beginner"},
                {"id": "database_design", "name": "Database Design", "level": "intermediate"},
                {"id": "microservices", "name": "Microservices Architecture", "level": "intermediate"},
                {"id": "distributed_systems", "name": "Distributed Systems", "level": "advanced"}
            ]
        elif category == "math":
            return [
                {"id": "calculus_limits", "name": "Limits", "level": "beginner", "subcategory": "calculus"},
                {"id": "calculus_derivatives", "name": "Derivatives", "level": "beginner", "subcategory": "calculus"},
                {"id": "linear_algebra_vectors", "name": "Vectors", "level": "beginner", "subcategory": "linear_algebra"},
                {"id": "statistics_descriptive", "name": "Descriptive Statistics", "level": "beginner", "subcategory": "statistics"}
            ]
        return []

def get_topic_details(topic_id, category="dsa"):
    """Get detailed information about a specific topic"""
    try:
        if category == "dsa":
            response = requests.get(f"{API_URL}/dsa/topics/{topic_id}")
        elif category == "system_design":
            response = requests.get(f"{API_URL}/system_design/topics/{topic_id}")
        elif category == "math":
            response = requests.get(f"{API_URL}/math/topics/{topic_id}")
        else:
            return {"error": "Invalid category"}
        
        return response.json()
    except Exception as e:
        # Return basic info as fallback
        return {
            "id": topic_id,
            "name": topic_id.replace('_', ' ').title(),
            "description": f"Comprehensive overview of {topic_id.replace('_', ' ').title()}.",
            "level": "beginner"
        }

def get_problems(topic_id, category="dsa", difficulty="all"):
    """Get problems for a specific topic"""
    try:
        if category == "dsa":
            response = requests.get(f"{API_URL}/exercise/problems/{topic_id}?difficulty={difficulty}")
        elif category == "math":
            response = requests.get(f"{API_URL}/math/problems/{topic_id}?difficulty={difficulty}")
        elif category == "system_design":
            response = requests.get(f"{API_URL}/system_design/exercise/{topic_id}?difficulty={difficulty}")
        else:
            return []
        
        return response.json()
    except Exception as e:
        # Return mock data as fallback
        return [
            {"id": f"{topic_id}_1", "title": f"{topic_id.replace('_', ' ').title()} Problem 1", "difficulty": "easy"},
            {"id": f"{topic_id}_2", "title": f"{topic_id.replace('_', ' ').title()} Problem 2", "difficulty": "medium"},
            {"id": f"{topic_id}_3", "title": f"{topic_id.replace('_', ' ').title()} Problem 3", "difficulty": "hard"}
        ]

def explain_concept(concept, category="dsa", level="beginner"):
    """Get an explanation for a specific concept"""
    try:
        response = requests.post(
            f"{API_URL}/tutor/explain", 
            json={"concept": concept, "category": category, "level": level}
        )
        return response.json().get("explanation", "")
    except Exception as e:
        # Return generic explanation as fallback
        return f"An explanation about {concept} would be provided here. This concept is part of {category} at {level} level."

# Sidebar navigation
def render_sidebar():
    """Render the sidebar navigation"""
    # App Title
    st.sidebar.markdown('<div class="main-header">Algo Ustadh</div>', unsafe_allow_html=True)
    st.sidebar.markdown("Your interactive professor for Computer Science fundamentals")
    
    # Category selection
    st.sidebar.markdown('<div class="sidebar-title">Learning Categories</div>', unsafe_allow_html=True)
    
    categories = get_categories()
    
    # Create buttons for each category
    col1, col2, col3 = st.sidebar.columns(3)
    
    if col1.button("📊 DSA", 
                  help="Data Structures & Algorithms", 
                  use_container_width=True,
                  type="primary" if st.session_state.current_category == "dsa" else "secondary"):
        st.session_state.current_category = "dsa"
        st.session_state.current_topic = None
        st.session_state.current_problem = None
    
    if col2.button("🏗️ System Design", 
                  help="System Design concepts and principles", 
                  use_container_width=True,
                  type="primary" if st.session_state.current_category == "system_design" else "secondary"):
        st.session_state.current_category = "system_design"
        st.session_state.current_topic = None
        st.session_state.current_problem = None
    
    if col3.button("🧮 Math", 
                  help="Mathematics for Computer Science", 
                  use_container_width=True,
                  type="primary" if st.session_state.current_category == "math" else "secondary"):
        st.session_state.current_category = "math"
        st.session_state.current_topic = None
        st.session_state.current_problem = None
    
    # Horizontal line
    st.sidebar.markdown("---")
    
    # Topics section based on selected category
    st.sidebar.markdown(f"<div class='sidebar-title'>Topics</div>", unsafe_allow_html=True)
    
    # Get topics for the current category
    topics = get_topics(st.session_state.current_category)
    
    # Special handling for math category - group by subcategory
    if st.session_state.current_category == "math":
        # Group topics by subcategory
        subcategories = {}
        for topic in topics:
            subcategory = topic.get('subcategory', 'Other')
            if subcategory not in subcategories:
                subcategories[subcategory] = []
            subcategories[subcategory].append(topic)
        
        # Display topics by subcategory
        for subcategory, subtopics in subcategories.items():
            with st.sidebar.expander(f"📚 {subcategory.replace('_', ' ').title()}", expanded=True):
                for topic in subtopics:
                    if st.button(topic["name"], key=f"btn_{topic['id']}", use_container_width=True):
                        st.session_state.current_topic = topic
                        st.session_state.current_problem = None
    else:
        # Group topics by level for other categories
        levels = {
            "beginner": [t for t in topics if t.get("level") == "beginner"],
            "intermediate": [t for t in topics if t.get("level") == "intermediate"],
            "advanced": [t for t in topics if t.get("level") == "advanced"]
        }
        
        # Create collapsible sections for each level
        with st.sidebar.expander("🌱 Beginner", expanded=True):
            for topic in levels["beginner"]:
                if st.button(topic["name"], key=f"btn_{topic['id']}", use_container_width=True):
                    st.session_state.current_topic = topic
                    st.session_state.current_problem = None
        
        with st.sidebar.expander("🔄 Intermediate", expanded=False):
            for topic in levels["intermediate"]:
                if st.button(topic["name"], key=f"btn_{topic['id']}", use_container_width=True):
                    st.session_state.current_topic = topic
                    st.session_state.current_problem = None
        
        with st.sidebar.expander("🔥 Advanced", expanded=False):
            for topic in levels["advanced"]:
                if st.button(topic["name"], key=f"btn_{topic['id']}", use_container_width=True):
                    st.session_state.current_topic = topic
                    st.session_state.current_problem = None
    
    # Learning tools section
    st.sidebar.markdown("---")
    st.sidebar.markdown('<div class="sidebar-title">Learning Tools</div>', unsafe_allow_html=True)
    
    col1, col2 = st.sidebar.columns(2)
    if col1.button("📊 My Progress", use_container_width=True):
        # TODO: Implement progress tracking view
        st.sidebar.info("Progress tracking coming soon!")
    
    if col2.button("📝 My Notes", use_container_width=True):
        # TODO: Implement notes view
        st.sidebar.info("Notes feature coming soon!")
    
    # User profile
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"Logged in as: **{st.session_state.user_id}**")

# Render landing page
def render_landing_page():
    """Render the landing page"""
    st.markdown('<div class="main-header">Welcome to Algo Ustadh</div>', unsafe_allow_html=True)
    st.markdown("""
    Your interactive professor for mastering Computer Science fundamentals in a step-by-step, engaging way.
    """)
    
    # Explanation of the name
    st.markdown("""
    > *"Ustadh" (أستاذ) means "Professor" in Arabic. Algo Ustadh is your AI-powered professor for algorithms, 
    > system design, and mathematics.*
    """)
    
    # Main features grid
    colored_header("🚀 What You Can Learn", description="", color_name="blue-70")
    
    feature_col1, feature_col2, feature_col3 = st.columns(3)
    
    with feature_col1:
        st.markdown("""
        <div class="content-section">
            <h3>📊 Data Structures & Algorithms</h3>
            <ul>
                <li>Master fundamental data structures</li>
                <li>Learn algorithm design techniques</li>
                <li>Solve coding interview problems</li>
                <li>Analyze time and space complexity</li>
                <li>Visualize algorithms in action</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with feature_col2:
        st.markdown("""
        <div class="content-section">
            <h3>🏗️ System Design</h3>
            <ul>
                <li>Understand distributed systems</li>
                <li>Design scalable architectures</li>
                <li>Learn database scaling techniques</li>
                <li>Practice with real-world case studies</li>
                <li>Prepare for system design interviews</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with feature_col3:
        st.markdown("""
        <div class="content-section">
            <h3>🧮 Mathematics</h3>
            <ul>
                <li>Study calculus fundamentals</li>
                <li>Learn linear algebra concepts</li>
                <li>Master descriptive & inferential statistics</li>
                <li>Apply math to computer science problems</li>
                <li>Solve step-by-step math problems</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # How it works section
    colored_header("🛠️ How It Works", description="", color_name="blue-70")
    
    st.markdown("""
    <div class="content-section">
        <ol>
            <li><strong>Select a topic</strong> from the sidebar to begin learning</li>
            <li><strong>Read the concept</strong> explanation and study the interactive visualizations</li>
            <li><strong>Try practice problems</strong> with step-by-step guidance and hints</li>
            <li><strong>Submit your solutions</strong> for instant feedback and analysis</li>
            <li><strong>Track your progress</strong> as you master each concept</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Featured topics section
    colored_header("📚 Featured Topics", description="", color_name="blue-70")
    
    # Get topics from each category for featuring
    dsa_topics = get_topics("dsa")
    system_design_topics = get_topics("system_design")
    math_topics = get_topics("math")
    
    # Extract beginner topics from each category
    dsa_featured = [t for t in dsa_topics if t.get("level") == "beginner"][:2]
    system_design_featured = [t for t in system_design_topics if t.get("level") == "beginner"][:2]
    math_featured = [t for t in math_topics if t.get("level") == "beginner"][:2]
    
    # Create a grid of featured topics
    featured_grid = grid(3, 2, vertical_align="center")
    
    # Add DSA topics
    for topic in dsa_featured:
        featured_grid.markdown(f"""
        <div class="topic-card">
            <div class="topic-title">📊 {topic["name"]}</div>
            <div class="topic-desc">Learn the fundamentals of {topic["name"].lower()} and their applications in computer science.</div>
            <div class="badge-beginner">Beginner</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Add System Design topics
    for topic in system_design_featured:
        featured_grid.markdown(f"""
        <div class="topic-card">
            <div class="topic-title">🏗️ {topic["name"]}</div>
            <div class="topic-desc">Master the principles of {topic["name"].lower()} for building scalable systems.</div>
            <div class="badge-beginner">Beginner</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Add Math topics
    for topic in math_featured:
        featured_grid.markdown(f"""
        <div class="topic-card">
            <div class="topic-title">🧮 {topic["name"]}</div>
            <div class="topic-desc">Understand the mathematical concept of {topic["name"].lower()} and its applications.</div>
            <div class="badge-beginner">Beginner</div>
        </div>
        """, unsafe_allow_html=True)

# Render DSA topic page
def render_dsa_topic_page(topic):
    """Render the DSA topic page"""
    st.markdown(f'<div class="main-header">{topic["name"]}</div>', unsafe_allow_html=True)
    
    # Get detailed information about the topic
    topic_details = get_topic_details(topic["id"], "dsa")
    
    # Topic tabs
    learn_tab, practice_tab, visualize_tab = st.tabs(["📚 Learn", "💻 Practice", "📊 Visualize"])
    
    with learn_tab:
        st.markdown('<div class="concept-header">Concept Overview</div>', unsafe_allow_html=True)
        st.markdown(topic_details.get("description", ""))
        
        # Time and space complexity
        st.markdown('<div class="concept-header">Complexity Analysis</div>', unsafe_allow_html=True)
        complexity_cols = st.columns(2)
        with complexity_cols[0]:
            st.markdown("**Time Complexity**")
            
            # Handle different formats of time complexity information
            time_complexity = topic_details.get("time_complexity", "Varies by operation")
            if isinstance(time_complexity, dict):
                for operation, complexity in time_complexity.items():
                    st.markdown(f"- {operation.capitalize()}: {complexity}")
            else:
                st.markdown(time_complexity)
        
        with complexity_cols[1]:
            st.markdown("**Space Complexity**")
            space_complexity = topic_details.get("space_complexity", "Varies by implementation")
            if isinstance(space_complexity, dict):
                for operation, complexity in space_complexity.items():
                    st.markdown(f"- {operation.capitalize()}: {complexity}")
            else:
                st.markdown(space_complexity)
        
        # Implementation
        st.markdown('<div class="concept-header">Python Implementation</div>', unsafe_allow_html=True)
        
        # Get explanation from API
        explanation = explain_concept(topic["id"], "dsa", topic.get("level", "beginner"))
        st.markdown(explanation)
        
        # Common use cases
        st.markdown('<div class="concept-header">Common Applications</div>', unsafe_allow_html=True)
        
        # Handle use cases in different formats
        use_cases = topic_details.get("use_cases", [])
        if isinstance(use_cases, list):
            for use_case in use_cases:
                st.markdown(f"- {use_case}")
        else:
            st.markdown(use_cases)
        
        # Common pitfalls or misconceptions
        if "common_pitfalls" in topic_details or "misconceptions" in topic_details:
            st.markdown('<div class="concept-header">Common Pitfalls & Misconceptions</div>', unsafe_allow_html=True)
            pitfalls = topic_details.get("common_pitfalls", topic_details.get("misconceptions", []))
            
            if isinstance(pitfalls, list):
                for pitfall in pitfalls:
                    st.markdown(f"- {pitfall}")
            else:
                st.markdown(pitfalls)
    
    with practice_tab:
        st.markdown('<div class="concept-header">Practice Problems</div>', unsafe_allow_html=True)
        
        # Filter controls
        difficulty = st.selectbox("Difficulty", ["all", "easy", "medium", "hard"], key="dsa_difficulty")
        
        # Get problems for this topic
        problems = get_problems(topic["id"], "dsa", difficulty)
        
        if not problems:
            st.info("No problems available for this topic yet. Check back soon!")
        else:
            # Display problems as cards
            for i, problem in enumerate(problems):
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        difficulty_badge = f"<span class='badge-beginner'>Easy</span>"
                        if problem.get('difficulty') == 'medium':
                            difficulty_badge = f"<span class='badge-intermediate'>Medium</span>"
                        elif problem.get('difficulty') == 'hard':
                            difficulty_badge = f"<span class='badge-advanced'>Hard</span>"
                        
                        st.markdown(f"**{problem.get('title', f'Problem {i+1}')}** {difficulty_badge}", unsafe_allow_html=True)
                        if 'description' in problem:
                            st.markdown(problem['description'][:100] + "..." if len(problem['description']) > 100 else problem['description'])
                    
                    with col2:
                        if st.button("Solve", key=f"solve_{problem['id']}"):
                            st.session_state.current_problem = problem
                            st.session_state.code_solution = ""
                            st.session_state.evaluation_result = None
                    
                    st.markdown("---")
        
        # Display selected problem
        if st.session_state.current_problem and st.session_state.current_category == "dsa":
            problem = st.session_state.current_problem
            
            # Create a container for the problem
            with st.container():
                st.markdown(f'<div class="concept-header">{problem.get("title", "Problem")}</div>', unsafe_allow_html=True)
                
                # Problem description
                if 'description' in problem:
                    st.markdown(problem['description'])
                
                # Examples
                if 'examples' in problem:
                    st.markdown("#### Examples")
                    for i, example in enumerate(problem['examples']):
                        with st.expander(f"Example {i+1}", expanded=i==0):
                            if 'input' in example:
                                st.markdown(f"**Input:** `{example['input']}`")
                            if 'output' in example:
                                st.markdown(f"**Output:** `{example['output']}`")
                            if 'explanation' in example:
                                st.markdown(f"**Explanation:** {example['explanation']}")
                
                # Constraints
                if 'constraints' in problem:
                    st.markdown("#### Constraints")
                    constraints = problem['constraints']
                    if isinstance(constraints, list):
                        for constraint in constraints:
                            st.markdown(f"- {constraint}")
                    else:
                        st.markdown(constraints)
                
                # Hint level slider
                st.markdown("#### Learning Support")
                hint_level = st.slider("Hint Level", 0, 2, st.session_state.hint_level, 
                                      help="0: Basic hints, 1: More detailed hints, 2: Step-by-step guidance")
                
                if hint_level != st.session_state.hint_level:
                    st.session_state.hint_level = hint_level
                    st.rerun()
                
                # Show hints based on level
                if hint_level > 0 and 'hints' in problem:
                    st.markdown('<div class="hint-box">', unsafe_allow_html=True)
                    
                    hints = problem['hints']
                    if isinstance(hints, list) and len(hints) > 0:
                        if hint_level == 1 and len(hints) >= 1:
                            st.markdown(f"**Hint:** {hints[0]}")
                        elif hint_level == 2:
                            for i, hint in enumerate(hints[:min(3, len(hints))]):
                                st.markdown(f"**Hint {i+1}:** {hint}")
                    else:
                        st.markdown(f"**Hint:** {hints}")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # If maximum hint level, try to get a detailed walkthrough
                if hint_level == 2:
                    try:
                        response = requests.post(
                            f"{API_URL}/tutor/walkthrough", 
                            json={"problem_id": problem["id"], "hint_level": 2, "category": "dsa"}
                        )
                        walkthrough = response.json().get("walkthrough", "")
                        
                        if walkthrough:
                            with st.expander("Step-by-Step Walkthrough", expanded=False):
                                st.markdown(walkthrough)
                    except Exception as e:
                        pass  # Silently fail if walkthrough is not available
                
                # Code editor
                st.markdown("#### Your Solution")
                st.markdown("Implement your Python solution below:")
                
                # Pre-fill with function definition if not already present
                if not st.session_state.code_solution:
                    st.session_state.code_solution = """def solution(nums):
    # Your code here
    pass
"""
                
                code_solution = st.text_area("", st.session_state.code_solution, height=300, 
                                           key="solution_editor", label_visibility="collapsed")
                
                col1, col2 = st.columns([1, 5])
                with col1:
                    if st.button("Submit", type="primary"):
                        st.session_state.code_solution = code_solution
                        
                        # Call evaluation API
                        try:
                            response = requests.post(
                                f"{API_URL}/exercise/evaluate",
                                json={
                                    "problem_id": problem["id"],
                                    "code": code_solution,
                                    "language": "python"
                                }
                            )
                            st.session_state.evaluation_result = response.json()
                        except Exception as e:
                            st.session_state.evaluation_result = {
                                "error": str(e),
                                "passed": 0,
                                "total_tests": 3,
                                "test_results": []
                            }
                
                with col2:
                    if st.button("Reset Solution"):
                        st.session_state.code_solution = """def solution(nums):
    # Your code here
    pass
"""
                        st.session_state.evaluation_result = None
                        st.rerun()
                
                # Display evaluation results
                if st.session_state.evaluation_result:
                    result = st.session_state.evaluation_result
                    
                    if "error" in result and result["error"]:
                        st.markdown('<div class="error-box">', unsafe_allow_html=True)
                        st.markdown(f"**Error:** {result['error']}")
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        if result["passed"] == result["total_tests"]:
                            st.markdown('<div class="success-box">', unsafe_allow_html=True)
                            st.markdown(f"**All tests passed!** ({result['passed']}/{result['total_tests']})")
                            st.markdown(f"Execution time: {result.get('execution_time', 0):.6f} seconds")
                            st.markdown('</div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="error-box">', unsafe_allow_html=True)
                            st.markdown(f"**Tests passed:** {result['passed']}/{result['total_tests']}")
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Display test results
                        with st.expander("Test Results", expanded=result["passed"] != result["total_tests"]):
                            for test in result.get("test_results", []):
                                if test.get("passed"):
                                    st.success(f"Test {test['test_number']}: Passed")
                                else:
                                    st.error(f"Test {test['test_number']}: Failed")
                                    st.markdown(f"Input: `{test['input']}`")
                                    st.markdown(f"Expected: `{test['expected']}`")
                                    st.markdown(f"Actual: `{test['actual']}`")
                        
                        # Display code analysis if available
                        if "code_analysis" in result:
                            analysis = result["code_analysis"]
                            with st.expander("Code Analysis", expanded=True):
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.markdown(f"**Time Complexity:** {analysis.get('time_complexity', 'N/A')}")
                                    st.markdown(f"**Space Complexity:** {analysis.get('space_complexity', 'N/A')}")
                                
                                with col2:
                                    st.markdown(f"**Code Quality:** {analysis.get('code_quality', 'N/A')}")
                                
                                st.markdown("**Improvement Suggestions:**")
                                st.markdown(analysis.get('improvement_suggestions', 'N/A'))
    
    with visualize_tab:
        st.markdown('<div class="concept-header">Interactive Visualization</div>', unsafe_allow_html=True)
        st.markdown("Visualizations help you understand how data structures and algorithms work in practice.")
        
        # Based on topic, show appropriate visualizations
        if topic["id"] == "arrays":
            st.markdown("### Array Operations")
            
            # Sample array visualization
            array_size = st.slider("Array Size", 5, 20, 10)
            array_values = []
            cols = st.columns(array_size)
            
            for i in range(array_size):
                with cols[i]:
                    array_values.append(st.number_input(f"", value=i+1, key=f"array_{i}", label_visibility="collapsed"))
            
            st.markdown("### Array Operations")
            op_col1, op_col2, op_col3 = st.columns(3)
            
            with op_col1:
                if st.button("Insert Element"):
                    st.session_state.array_operation = "insert"
            
            with op_col2:
                if st.button("Delete Element"):
                    st.session_state.array_operation = "delete"
            
            with op_col3:
                if st.button("Search Element"):
                    st.session_state.array_operation = "search"
            
            # Animation placeholder
            st.markdown("### Visualization")
            st.info("Interactive visualizations for arrays will be available soon!")
            
        elif topic["id"] == "linked_lists":
            st.markdown("### Linked List Operations")
            
            # Linked list visualization with nodes and arrows
            fig = go.Figure()
            
            # Define number of nodes
            num_nodes = st.slider("Number of Nodes", 3, 10, 5)
            
            # Generate node positions
            x_positions = list(range(1, num_nodes + 1))
            y_positions = [1] * num_nodes
            node_values = list(range(1, num_nodes + 1))
            
            # Draw nodes
            fig.add_trace(go.Scatter(
                x=x_positions,
                y=y_positions,
                mode='markers+text',
                marker=dict(size=30, color='skyblue', line=dict(color='navy', width=2)),
                text=node_values,
                textposition="middle center",
                name='Nodes'
            ))
            
            # Draw arrows between nodes
            for i in range(num_nodes-1):
                fig.add_annotation(
                    x=x_positions[i]+0.5,
                    y=y_positions[i],
                    ax=x_positions[i]+0.1,
                    ay=y_positions[i],
                    xref="x",
                    yref="y",
                    axref="x",
                    ayref="y",
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=2,
                    arrowcolor='navy'
                )
            
            # Add null terminator
            fig.add_trace(go.Scatter(
                x=[x_positions[-1] + 1],
                y=[1],
                mode='text',
                text=['NULL'],
                textposition="middle center",
                name='NULL'
            ))
            
            # Update layout
            fig.update_layout(
                title="Linked List Visualization",
                xaxis=dict(range=[0, num_nodes + 2], showticklabels=False),
                yaxis=dict(range=[0, 2], showticklabels=False),
                showlegend=False,
                height=250,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Operations
            st.markdown("### Operations")
            op_col1, op_col2, op_col3, op_col4 = st.columns(4)
            
            with op_col1:
                if st.button("Insert at Head"):
                    st.info("Animation for inserting at head would be shown here")
            
            with op_col2:
                if st.button("Insert at Tail"):
                    st.info("Animation for inserting at tail would be shown here")
            
            with op_col3:
                if st.button("Delete Node"):
                    st.info("Animation for deleting a node would be shown here")
            
            with op_col4:
                if st.button("Reverse List"):
                    st.info("Animation for reversing the list would be shown here")
            
        else:
            # Generic placeholder for other topics
            st.info("Interactive visualizations for this topic will be available soon!")
            st.markdown("In the meantime, you can practice with the examples in the Practice tab.")

# Render System Design topic page
def render_system_design_topic_page(topic):
    """Render the System Design topic page"""
    st.markdown(f'<div class="main-header">{topic["name"]}</div>', unsafe_allow_html=True)
    
    # Get detailed information about the topic
    topic_details = get_topic_details(topic["id"], "system_design")
    
    # Topic tabs
    learn_tab, case_studies_tab, exercises_tab = st.tabs(["📚 Learn", "🏢 Case Studies", "💻 Exercises"])
    
    with learn_tab:
        st.markdown('<div class="concept-header">Concept Overview</div>', unsafe_allow_html=True)
        st.markdown(topic_details.get("description", ""))
        
        # Key components
        if "components" in topic_details:
            st.markdown('<div class="concept-header">Key Components</div>', unsafe_allow_html=True)
            components = topic_details.get("components", [])
            if isinstance(components, list):
                for component in components:
                    st.markdown(f"- {component}")
            else:
                st.markdown(components)
        
        # Implementation guidance
        st.markdown('<div class="concept-header">Design Principles</div>', unsafe_allow_html=True)
        
        # Get explanation from API
        explanation = explain_concept(topic["id"], "system_design", topic.get("level", "beginner"))
        st.markdown(explanation)
        
        # Trade-offs
        if "trade_offs" in topic_details:
            st.markdown('<div class="concept-header">Trade-offs</div>', unsafe_allow_html=True)
            trade_offs = topic_details.get("trade_offs", [])
            if isinstance(trade_offs, list):
                for trade_off in trade_offs:
                    st.markdown(f"- {trade_off}")
            else:
                st.markdown(trade_offs)
        
        # Best practices
        if "best_practices" in topic_details:
            st.markdown('<div class="concept-header">Best Practices</div>', unsafe_allow_html=True)
            best_practices = topic_details.get("best_practices", [])
            if isinstance(best_practices, list):
                for practice in best_practices:
                    st.markdown(f"- {practice}")
            else:
                st.markdown(best_practices)
        
        # Common use cases
        if "use_cases" in topic_details:
            st.markdown('<div class="concept-header">Common Applications</div>', unsafe_allow_html=True)
            use_cases = topic_details.get("use_cases", [])
            if isinstance(use_cases, list):
                for use_case in use_cases:
                    st.markdown(f"- {use_case}")
            else:
                st.markdown(use_cases)
    
    with case_studies_tab:
        st.markdown('<div class="concept-header">Real-world Case Studies</div>', unsafe_allow_html=True)
        st.markdown("Learn from real-world implementations and design decisions.")
        
        # Complexity selection
        complexity = st.selectbox("Complexity", ["simple", "medium", "complex"], index=1)
        
        # Try to get case study from API
        try:
            response = requests.get(
                f"{API_URL}/system_design/case_study/{topic['id']}?complexity={complexity}"
            )
            case_study = response.json().get("case_study", "")
            if case_study:
                st.markdown(case_study)
            else:
                raise Exception("No case study found")
        except Exception as e:
            # Fallback case study
            st.markdown(f"""
            ### Sample Case Study: Building a {topic["name"]} System
            
            *This is a simplified example to demonstrate the concept.*
            
            #### Scenario
            
            Imagine you're designing a photo-sharing application that needs to handle:
            
            - 10 million daily active users
            - 5 million photo uploads per day
            - Users follow each other creating a social graph
            - Global user base requiring low latency worldwide
            
            #### Key Challenges
            
            1. **Scale**: Handling millions of users and photos
            2. **Performance**: Ensuring fast load times for photos 
            3. **Reliability**: Maintaining high availability
            
            #### Sample Architecture Using {topic["name"]}
            
            *Here would be a detailed explanation with diagrams showing how {topic["name"].lower()} would be implemented in this system.*
            
            #### Key Decisions and Trade-offs
            
            *This section would explain the design choices made and alternative approaches that could have been used.*
            """)
    
    with exercises_tab:
        st.markdown('<div class="concept-header">Design Exercises</div>', unsafe_allow_html=True)
        st.markdown("Practice your system design skills with these exercises.")
        
        # Difficulty selection
        difficulty = st.selectbox("Difficulty", ["easy", "medium", "hard"], index=1, key="sd_difficulty")
        
        # Try to get exercises from API
        try:
            response = requests.get(
                f"{API_URL}/system_design/exercise/{topic['id']}?difficulty={difficulty}"
            )
            exercise = response.json().get("exercise", "")
            if exercise:
                st.markdown(exercise)
            else:
                raise Exception("No exercise found")
        except Exception as e:
            # Fallback exercise
            st.markdown(f"""
            ### Exercise: Design a {topic["name"]} for a Social Media Platform
            
            #### Requirements:
            
            1. The platform has 50 million daily active users
            2. Users can post status updates, photos, and short videos
            3. Users can follow other users (asymmetric relationship)
            4. The feed should show content from followed users
            5. The system should support hashtag search
            
            #### Task:
            
            Design a system that focuses on the {topic["name"].lower()} aspect, addressing:
            
            1. How would you implement {topic["name"].lower()} for this use case?
            2. What are the key components needed?
            3. What trade-offs would you consider?
            4. How would you ensure reliability and fault tolerance?
            
            #### Deliverables:
            
            1. High-level architecture diagram
            2. Explanation of key components
            3. Discussion of trade-offs and design decisions
            4. Consideration of failure scenarios and how to handle them
            """)
        
        # Solution submission
        st.markdown("#### Your Solution")
        design_solution = st.text_area("Enter your design solution here (use markdown for formatting if needed):", 
                                      value=st.session_state.design_solution, height=300)
        
        if st.button("Submit Design", key="submit_design"):
            st.session_state.design_solution = design_solution
            
            # Call review API
            try:
                response = requests.post(
                    f"{API_URL}/system_design/review",
                    json={
                        "topic_id": topic["id"],
                        "design": design_solution
                    }
                )
                review = response.json().get("review", "")
                
                if review:
                    st.markdown("### Expert Review")
                    st.markdown(review)
                else:
                    st.warning("No feedback available at this time. Please try again later.")
            except Exception as e:
                st.error(f"Error getting feedback: {str(e)}")

# Render Math topic page
def render_math_topic_page(topic):
    """Render the Math topic page"""
    subcategory = topic.get("subcategory", "").replace("_", " ").title()
    st.markdown(f'<div class="main-header">{topic["name"]} ({subcategory})</div>', unsafe_allow_html=True)
    
    # Get detailed information about the topic
    topic_details = get_topic_details(topic["id"], "math")
    
    # Topic tabs
    learn_tab, problems_tab, interactive_tab = st.tabs(["📚 Learn", "📝 Problems", "🧮 Interactive"])
    
    with learn_tab:
        st.markdown('<div class="concept-header">Concept Overview</div>', unsafe_allow_html=True)
        st.markdown(topic_details.get("description", ""))
        
        # Key formulas
        if "key_formulas" in topic_details:
            st.markdown('<div class="concept-header">Key Formulas</div>', unsafe_allow_html=True)
            formulas = topic_details.get("key_formulas", [])
            if isinstance(formulas, list):
                for formula in formulas:
                    st.markdown(f"- {formula}")
            else:
                st.markdown(formulas)
        
        # Explanation
        st.markdown('<div class="concept-header">Detailed Explanation</div>', unsafe_allow_html=True)
        
        # Get explanation from API
        explanation = explain_concept(topic["id"], "math", topic.get("level", "beginner"))
        st.markdown(explanation)
        
        # Applications
        if "applications" in topic_details:
            st.markdown('<div class="concept-header">Applications</div>', unsafe_allow_html=True)
            applications = topic_details.get("applications", [])
            if isinstance(applications, list):
                for application in applications:
                    st.markdown(f"- {application}")
            else:
                st.markdown(applications)
        
        # Common misconceptions
        if "misconceptions" in topic_details:
            st.markdown('<div class="concept-header">Common Misconceptions</div>', unsafe_allow_html=True)
            misconceptions = topic_details.get("misconceptions", [])
            if isinstance(misconceptions, list):
                for misconception in misconceptions:
                    st.markdown(f"- {misconception}")
            else:
                st.markdown(misconceptions)
        
        # Related concepts
        if "related_concepts" in topic_details:
            st.markdown('<div class="concept-header">Related Concepts</div>', unsafe_allow_html=True)
            related = topic_details.get("related_concepts", [])
            if isinstance(related, list):
                for concept in related:
                    st.markdown(f"- {concept}")
            else:
                st.markdown(related)
    
    with problems_tab:
        st.markdown('<div class="concept-header">Practice Problems</div>', unsafe_allow_html=True)
        
        # Filter controls
        difficulty = st.selectbox("Difficulty", ["all", "easy", "medium", "hard"], key="math_difficulty")
        
        # Get problems for this topic
        problems = get_problems(topic["id"], "math", difficulty)
        
        if not problems:
            st.info("No problems available for this topic yet. Check back soon!")
        else:
            # Display problems as cards
            for i, problem in enumerate(problems):
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        difficulty_badge = f"<span class='badge-beginner'>Easy</span>"
                        if problem.get('difficulty') == 'medium':
                            difficulty_badge = f"<span class='badge-intermediate'>Medium</span>"
                        elif problem.get('difficulty') == 'hard':
                            difficulty_badge = f"<span class='badge-advanced'>Hard</span>"
                        
                        title = problem.get('title', problem.get('problem', f'Problem {i+1}'))
                        st.markdown(f"**{title}** {difficulty_badge}", unsafe_allow_html=True)
                        
                        # Show the problem statement (truncated if too long)
                        problem_text = problem.get('problem', '')
                        if len(problem_text) > 100:
                            st.markdown(problem_text[:100] + "...")
                        else:
                            st.markdown(problem_text)
                    
                    with col2:
                        if st.button("Solve", key=f"solve_{problem['id']}"):
                            st.session_state.current_problem = problem
                            st.session_state.math_solution = ""
                    
                    st.markdown("---")
        
        # Display selected problem
        if st.session_state.current_problem and st.session_state.current_category == "math":
            problem = st.session_state.current_problem
            
            # Create a container for the problem
            with st.container():
                title = problem.get('title', 'Math Problem')
                st.markdown(f'<div class="concept-header">{title}</div>', unsafe_allow_html=True)
                
                # Problem statement
                problem_text = problem.get('problem', '')
                st.markdown(problem_text)
                
                # Solution steps controlled by checkbox
                show_steps = st.checkbox("Show step-by-step solution", value=False)
                
                if show_steps and 'solution_steps' in problem:
                    st.markdown('<div class="hint-box">', unsafe_allow_html=True)
                    st.markdown("### Solution Steps")
                    st.markdown(problem['solution_steps'])
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Your solution
                st.markdown("### Your Solution")
                math_solution = st.text_area("Enter your solution:", value=st.session_state.math_solution, height=150)
                
                if st.button("Check Solution", key="check_math"):
                    st.session_state.math_solution = math_solution
                    
                    # Display the answer
                    st.markdown('<div class="info-box">', unsafe_allow_html=True)
                    st.markdown("### Correct Answer")
                    st.markdown(problem.get('answer', 'Solution not available'))
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Try to get feedback on solution
                    try:
                        response = requests.post(
                            f"{API_URL}/math/check",
                            json={
                                "problem": problem_text,
                                "solution": math_solution
                            }
                        )
                        feedback = response.json().get("feedback", "")
                        
                        if feedback:
                            st.markdown("### Feedback on Your Solution")
                            st.markdown(feedback)
                    except Exception as e:
                        # Silently fail if feedback not available
                        pass
    
    with interactive_tab:
        st.markdown('<div class="concept-header">Interactive Exploration</div>', unsafe_allow_html=True)
        
        # Different interactive tools based on the math subcategory
        subcategory = topic.get("subcategory", "")
        
        if subcategory == "calculus":
            st.markdown("### Interactive Calculus Tools")
            
            # Function explorer
            st.markdown("#### Function Explorer")
            
            # Input for function
            function_input = st.text_input("Enter a function (e.g., x^2, sin(x), e^x):", "x^2")
            
            # Range for x values
            x_min, x_max = st.slider("x-axis range:", -10.0, 10.0, (-5.0, 5.0))
            
            # Create plot
            x = np.linspace(x_min, x_max, 1000)
            
            # Parse the function input (simple cases only)
            y = None
            try:
                # Replace common functions with numpy equivalents
                function = function_input.replace("^", "**")
                function = function.replace("sin", "np.sin")
                function = function.replace("cos", "np.cos")
                function = function.replace("tan", "np.tan")
                function = function.replace("exp", "np.exp")
                function = function.replace("log", "np.log")
                function = function.replace("e^", "np.exp(")
                if "e^" in function_input:
                    function = function + ")"
                
                # Evaluate the function
                y = eval(function.replace("x", "(x)"))
                
                # Plot the function
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(x, y, 'b-', linewidth=2)
                ax.grid(True)
                ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
                ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)
                ax.set_xlabel('x')
                ax.set_ylabel('y')
                ax.set_title(f'Function: f(x) = {function_input}')
                
                # If derivative option is selected, plot it
                if st.checkbox("Show derivative"):
                    # Simple numerical derivative
                    dy = np.gradient(y, x)
                    ax.plot(x, dy, 'r--', linewidth=2, label="f'(x)")
                    ax.legend()
                
                st.pyplot(fig)
                
            except Exception as e:
                st.error(f"Error plotting function: {str(e)}")
                st.info("Try simple functions like 'x^2', 'sin(x)', or 'x^2 + 2*x + 1'")
        
        elif subcategory == "linear_algebra":
            st.markdown("### Linear Algebra Tools")
            
            # Matrix operations
            st.markdown("#### Matrix Operations")
            
            # Create a 2x2 or 3x3 matrix
            matrix_size = st.radio("Matrix size:", ["2x2", "3x3"])
            
            if matrix_size == "2x2":
                st.markdown("Enter values for Matrix A:")
                
                # Create 2x2 grid for input
                a11 = st.number_input("A[1,1]:", value=1.0, key="a11")
                a12 = st.number_input("A[1,2]:", value=2.0, key="a12")
                a21 = st.number_input("A[2,1]:", value=3.0, key="a21")
                a22 = st.number_input("A[2,2]:", value=4.0, key="a22")
                
                # Create the matrix
                matrix_a = np.array([[a11, a12], [a21, a22]])
                
                # Display the matrix
                st.markdown("#### Matrix A:")
                st.text(f"{matrix_a[0,0]} {matrix_a[0,1]}\n{matrix_a[1,0]} {matrix_a[1,1]}")
                
                # Matrix operations
                st.markdown("#### Matrix Properties:")
                
                # Determinant
                det_a = np.linalg.det(matrix_a)
                st.markdown(f"**Determinant**: {det_a:.4f}")
                
                # Eigenvalues and eigenvectors
                try:
                    eigenvalues, eigenvectors = np.linalg.eig(matrix_a)
                    st.markdown(f"**Eigenvalues**: {eigenvalues[0]:.4f}, {eigenvalues[1]:.4f}")
                    
                    # Trace
                    trace_a = np.trace(matrix_a)
                    st.markdown(f"**Trace**: {trace_a}")
                    
                    # Inverse
                    if det_a != 0:
                        inv_a = np.linalg.inv(matrix_a)
                        st.markdown("**Inverse Matrix**:")
                        st.text(f"{inv_a[0,0]:.4f} {inv_a[0,1]:.4f}\n{inv_a[1,0]:.4f} {inv_a[1,1]:.4f}")
                    else:
                        st.warning("Matrix is singular, cannot compute inverse.")
                
                except Exception as e:
                    st.error(f"Error computing matrix properties: {str(e)}")
            
            else:  # 3x3 matrix
                st.markdown("Enter values for Matrix A (3x3):")
                
                # Simple representation for demo
                st.warning("3x3 matrix input not fully implemented in this demo.")
                
                # Create a sample 3x3 matrix
                matrix_a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
                
                # Display the matrix
                st.markdown("#### Sample Matrix A:")
                st.text(f"{matrix_a[0,0]} {matrix_a[0,1]} {matrix_a[0,2]}\n{matrix_a[1,0]} {matrix_a[1,1]} {matrix_a[1,2]}\n{matrix_a[2,0]} {matrix_a[2,1]} {matrix_a[2,2]}")
                
                # Matrix operations
                st.markdown("#### Matrix Properties:")
                
                # Determinant
                det_a = np.linalg.det(matrix_a)
                st.markdown(f"**Determinant**: {det_a:.4f}")
                
                # Eigenvalues
                eigenvalues = np.linalg.eigvals(matrix_a)
                st.markdown(f"**Eigenvalues**: {eigenvalues[0]:.4f}, {eigenvalues[1]:.4f}, {eigenvalues[2]:.4f}")
                
                # Trace
                trace_a = np.trace(matrix_a)
                st.markdown(f"**Trace**: {trace_a}")
        
        elif subcategory == "statistics":
            st.markdown("### Statistical Analysis Tools")
            
            # Data generation or input
            st.markdown("#### Generate Sample Data")
            
            # Choose distribution
            distribution = st.selectbox("Select distribution:", 
                                       ["Normal", "Uniform", "Exponential", "Binomial"])
            
            # Parameters based on distribution
            if distribution == "Normal":
                mean = st.slider("Mean:", -10.0, 10.0, 0.0)
                std = st.slider("Standard Deviation:", 0.1, 10.0, 1.0)
                n_samples = st.slider("Number of samples:", 10, 1000, 100)
                
                # Generate data
                data = np.random.normal(mean, std, n_samples)
            
            elif distribution == "Uniform":
                low = st.slider("Lower bound:", -10.0, 10.0, 0.0)
                high = st.slider("Upper bound:", low + 0.1, 20.0, 1.0)
                n_samples = st.slider("Number of samples:", 10, 1000, 100)
                
                # Generate data
                data = np.random.uniform(low, high, n_samples)
            
            elif distribution == "Exponential":
                scale = st.slider("Scale (λ):", 0.1, 10.0, 1.0)
                n_samples = st.slider("Number of samples:", 10, 1000, 100)
                
                # Generate data
                data = np.random.exponential(scale, n_samples)
            
            else:  # Binomial
                n = st.slider("Number of trials (n):", 1, 100, 10)
                p = st.slider("Probability of success (p):", 0.0, 1.0, 0.5)
                n_samples = st.slider("Number of samples:", 10, 1000, 100)
                
                # Generate data
                data = np.random.binomial(n, p, n_samples)
            
            # Display generated data
            st.markdown("#### Generated Data")
            show_raw_data = st.checkbox("Show raw data")
            if show_raw_data:
                st.write(data)
            
            # Data visualization
            st.markdown("#### Data Visualization")
            
            # Histogram
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(data, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
            ax.set_xlabel('Value')
            ax.set_ylabel('Frequency')
            ax.set_title(f'Histogram of {distribution} Distribution')
            ax.grid(alpha=0.3)
            st.pyplot(fig)
            
            # Descriptive statistics
            st.markdown("#### Descriptive Statistics")
            
            # Calculate statistics
            mean = np.mean(data)
            median = np.median(data)
            std = np.std(data)
            min_val = np.min(data)
            max_val = np.max(data)
            
            # Display statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Mean", f"{mean:.4f}")
                st.metric("Standard Deviation", f"{std:.4f}")
            
            with col2:
                st.metric("Median", f"{median:.4f}")
                st.metric("Range", f"{max_val - min_val:.4f}")
            
            with col3:
                st.metric("Minimum", f"{min_val:.4f}")
                st.metric("Maximum", f"{max_val:.4f}")
            
            # Confidence interval for mean
            confidence = 0.95
            z_score = 1.96  # For 95% confidence
            
            ci_low = mean - z_score * (std / np.sqrt(n_samples))
            ci_high = mean + z_score * (std / np.sqrt(n_samples))
            
            st.markdown(f"**{confidence*100:.0f}% Confidence Interval for Mean**: ({ci_low:.4f}, {ci_high:.4f})")
        
        else:
            # Generic placeholder for other topics
            st.info("Interactive tools for this topic will be available soon!")

# Main app logic
def main():
    # Render the sidebar
    render_sidebar()
    
    # Determine what to render in the main area
    if st.session_state.current_topic is None:
        # Show landing page
        render_landing_page()
    else:
        # Show topic page based on category
        if st.session_state.current_category == "dsa":
            render_dsa_topic_page(st.session_state.current_topic)
        elif st.session_state.current_category == "system_design":
            render_system_design_topic_page(st.session_state.current_topic)
        elif st.session_state.current_category == "math":
            render_math_topic_page(st.session_state.current_topic)

if __name__ == "__main__":
    main()