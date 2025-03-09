import os
import json
import sqlite3
import argparse

def init_database(reset=False):
    """Initialize the database with schema and seed data"""
    print("Initializing AlgoMentor database...")
    
    # Create data directory if it doesn't exist
    os.makedirs("backend/data", exist_ok=True)
    
    # Database file path
    db_path = "backend/data/algomentor.db"
    
    # If reset flag is set, remove existing database
    if reset and os.path.exists(db_path):
        os.remove(db_path)
        print("Existing database removed.")
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create tables
    print("Creating tables...")
    with open("backend/models/schema.sql", "r") as f:
        schema_sql = f.read()
        cursor.executescript(schema_sql)
    
    # Load and insert topics
    print("Seeding topics...")
    with open("backend/data/topics.json", "r") as f:
        topics = json.load(f)
        for topic in topics:
            cursor.execute(
                "INSERT OR REPLACE INTO topics (id, name, description, level, order_num) VALUES (?, ?, ?, ?, ?)",
                (topic["id"], topic["name"], topic["description"], topic["level"], topic.get("order", 0))
            )
    
    # Load and insert problems
    print("Seeding problems...")
    try:
        with open("backend/data/problems.json", "r") as f:
            problems = json.load(f)
            for problem in problems:
                cursor.execute(
                    """INSERT OR REPLACE INTO problems 
                       (id, topic_id, title, description, difficulty, hints, solution, test_cases) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        problem["id"], 
                        problem["topic_id"], 
                        problem["title"], 
                        problem["description"], 
                        problem["difficulty"],
                        json.dumps(problem.get("hints", [])), 
                        problem.get("solution", ""),
                        json.dumps(problem.get("test_cases", []))
                    )
                )
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Warning: Could not load problems: {e}")
    
    # Create demo user
    print("Creating demo user...")
    cursor.execute(
        "INSERT OR IGNORE INTO users (id, username, email) VALUES (?, ?, ?)",
        ("demo_user", "demo", "demo@example.com")
    )
    
    # Commit changes
    conn.commit()
    conn.close()
    
    print("Database initialization complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initialize AlgoMentor database")
    parser.add_argument("--reset", action="store_true", help="Reset existing database")
    args = parser.parse_args()
    
    init_database(reset=args.reset)