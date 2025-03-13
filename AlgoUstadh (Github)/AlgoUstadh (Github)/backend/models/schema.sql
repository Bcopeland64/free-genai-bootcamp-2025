-- Topics table
CREATE TABLE IF NOT EXISTS topics (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    category TEXT NOT NULL,  -- 'dsa', 'system_design', or 'math'
    subcategory TEXT,        -- For math: 'calculus', 'linear_algebra', 'statistics'
    level TEXT NOT NULL,
    order_num INTEGER NOT NULL
);

-- Problems table
CREATE TABLE IF NOT EXISTS problems (
    id TEXT PRIMARY KEY,
    topic_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    hints TEXT,
    solution TEXT,
    test_cases TEXT,
    FOREIGN KEY (topic_id) REFERENCES topics (id)
);

-- System Design Exercises table
CREATE TABLE IF NOT EXISTS system_design_exercises (
    id TEXT PRIMARY KEY,
    topic_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    requirements TEXT NOT NULL,
    example_solution TEXT,
    evaluation_criteria TEXT,
    FOREIGN KEY (topic_id) REFERENCES topics (id)
);

-- Math Problems table
CREATE TABLE IF NOT EXISTS math_problems (
    id TEXT PRIMARY KEY,
    topic_id TEXT NOT NULL,
    problem TEXT NOT NULL,
    answer TEXT NOT NULL,
    solution_steps TEXT,
    difficulty TEXT NOT NULL,
    tags TEXT,
    FOREIGN KEY (topic_id) REFERENCES topics (id)
);

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Progress table
CREATE TABLE IF NOT EXISTS progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    topic_id TEXT NOT NULL,
    item_id TEXT,          -- Can be problem_id, exercise_id, or math_problem_id
    item_type TEXT NOT NULL, -- 'problem', 'exercise', or 'math_problem'
    status TEXT NOT NULL,
    completed BOOLEAN DEFAULT 0,
    last_attempt TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (topic_id) REFERENCES topics (id)
);

-- User Notes table
CREATE TABLE IF NOT EXISTS user_notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    topic_id TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (topic_id) REFERENCES topics (id)
);

-- Learning Paths table
CREATE TABLE IF NOT EXISTS learning_paths (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    category TEXT NOT NULL,  -- 'dsa', 'system_design', or 'math'
    difficulty TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Learning Path Topics table (for many-to-many relationship)
CREATE TABLE IF NOT EXISTS learning_path_topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    learning_path_id INTEGER NOT NULL,
    topic_id TEXT NOT NULL,
    order_num INTEGER NOT NULL,
    FOREIGN KEY (learning_path_id) REFERENCES learning_paths (id),
    FOREIGN KEY (topic_id) REFERENCES topics (id)
);