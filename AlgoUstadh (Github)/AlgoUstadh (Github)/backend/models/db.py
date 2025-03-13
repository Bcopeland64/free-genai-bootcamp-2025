import sqlite3
import os
import json
from flask import g

DATABASE_PATH = "backend/data/algomentor.db"

def get_db():
    """Get database connection, creating it if needed"""
    db = getattr(g, '_database', None)
    if db is None:
        os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
        db = g._database = sqlite3.connect(DATABASE_PATH)
        db.row_factory = sqlite3.Row
    return db

def init_db(app):
    """Initialize the database with required tables"""
    with app.app_context():
        db = get_db()
        with app.open_resource('models/schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

def query_db(query, args=(), one=False):
    """Query the database"""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def insert_db(query, args=()):
    """Insert into the database"""
    db = get_db()
    cur = db.execute(query, args)
    db.commit()
    last_id = cur.lastrowid
    cur.close()
    return last_id

def seed_topics():
    """Seed the database with initial DSA topics"""
    db = get_db()
    
    # Check if topics already exist
    topics_exist = query_db("SELECT COUNT(*) FROM topics", one=True)
    if topics_exist and topics_exist[0] > 0:
        return
    
    # Load topics from JSON
    with open('backend/data/topics.json', 'r') as f:
        topics = json.load(f)
    
    # Insert topics
    for topic in topics:
        insert_db(
            "INSERT INTO topics (id, name, description, level, order_num) VALUES (?, ?, ?, ?, ?)",
            (topic['id'], topic['name'], topic['description'], topic['level'], topic['order'])
        )
    
    db.commit()