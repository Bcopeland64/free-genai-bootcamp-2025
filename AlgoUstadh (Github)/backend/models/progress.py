from backend.models.db import query_db, insert_db

class UserProgress:
    """Class for managing user learning progress"""
    
    @staticmethod
    def get_progress(user_id, category='all'):
        """Get the learning progress for a specific user"""
        if category == 'dsa':
            # Get DSA topics progress
            topics_progress = query_db(
                """
                SELECT t.id, t.name, t.level, t.category, t.subcategory,
                      COUNT(DISTINCT p.id) AS total_problems,
                      COUNT(DISTINCT CASE WHEN pr.completed = 1 THEN p.id END) AS completed_problems
                FROM topics t
                LEFT JOIN problems p ON p.topic_id = t.id
                LEFT JOIN progress pr ON pr.topic_id = t.id AND pr.item_id = p.id 
                    AND pr.item_type = 'problem' AND pr.user_id = ?
                WHERE t.category = 'dsa'
                GROUP BY t.id
                ORDER BY t.order_num
                """,
                [user_id]
            )
        elif category == 'system_design':
            # Get System Design topics progress
            topics_progress = query_db(
                """
                SELECT t.id, t.name, t.level, t.category, t.subcategory,
                      COUNT(DISTINCT e.id) AS total_exercises,
                      COUNT(DISTINCT CASE WHEN pr.completed = 1 THEN e.id END) AS completed_exercises
                FROM topics t
                LEFT JOIN system_design_exercises e ON e.topic_id = t.id
                LEFT JOIN progress pr ON pr.topic_id = t.id AND pr.item_id = e.id 
                    AND pr.item_type = 'exercise' AND pr.user_id = ?
                WHERE t.category = 'system_design'
                GROUP BY t.id
                ORDER BY t.order_num
                """,
                [user_id]
            )
        elif category == 'math':
            # Get Math topics progress
            topics_progress = query_db(
                """
                SELECT t.id, t.name, t.level, t.category, t.subcategory,
                      COUNT(DISTINCT mp.id) AS total_problems,
                      COUNT(DISTINCT CASE WHEN pr.completed = 1 THEN mp.id END) AS completed_problems
                FROM topics t
                LEFT JOIN math_problems mp ON mp.topic_id = t.id
                LEFT JOIN progress pr ON pr.topic_id = t.id AND pr.item_id = mp.id 
                    AND pr.item_type = 'math_problem' AND pr.user_id = ?
                WHERE t.category = 'math'
                GROUP BY t.id
                ORDER BY t.order_num
                """,
                [user_id]
            )
        else:
            # Get all topics progress
            topics_progress = query_db(
                """
                SELECT t.id, t.name, t.level, t.category, t.subcategory,
                      COALESCE(dsa.total_problems, 0) + 
                      COALESCE(sd.total_exercises, 0) + 
                      COALESCE(math.total_problems, 0) AS total_items,
                      
                      COALESCE(dsa.completed_problems, 0) + 
                      COALESCE(sd.completed_exercises, 0) + 
                      COALESCE(math.completed_problems, 0) AS completed_items
                      
                FROM topics t
                
                LEFT JOIN (
                    SELECT p.topic_id,
                          COUNT(DISTINCT p.id) AS total_problems,
                          COUNT(DISTINCT CASE WHEN pr.completed = 1 THEN p.id END) AS completed_problems
                    FROM problems p
                    LEFT JOIN progress pr ON pr.item_id = p.id AND pr.item_type = 'problem' AND pr.user_id = ?
                    GROUP BY p.topic_id
                ) dsa ON dsa.topic_id = t.id AND t.category = 'dsa'
                
                LEFT JOIN (
                    SELECT e.topic_id,
                          COUNT(DISTINCT e.id) AS total_exercises,
                          COUNT(DISTINCT CASE WHEN pr.completed = 1 THEN e.id END) AS completed_exercises
                    FROM system_design_exercises e
                    LEFT JOIN progress pr ON pr.item_id = e.id AND pr.item_type = 'exercise' AND pr.user_id = ?
                    GROUP BY e.topic_id
                ) sd ON sd.topic_id = t.id AND t.category = 'system_design'
                
                LEFT JOIN (
                    SELECT mp.topic_id,
                          COUNT(DISTINCT mp.id) AS total_problems,
                          COUNT(DISTINCT CASE WHEN pr.completed = 1 THEN mp.id END) AS completed_problems
                    FROM math_problems mp
                    LEFT JOIN progress pr ON pr.item_id = mp.id AND pr.item_type = 'math_problem' AND pr.user_id = ?
                    GROUP BY mp.topic_id
                ) math ON math.topic_id = t.id AND t.category = 'math'
                
                ORDER BY t.category, t.order_num
                """,
                [user_id, user_id, user_id]
            )
        
        # Format the results
        result = []
        for topic in topics_progress:
            topic_dict = dict(topic)
            
            # Calculate completion percentage
            if category == 'dsa':
                total = topic_dict.get('total_problems', 0)
                completed = topic_dict.get('completed_problems', 0)
            elif category == 'system_design':
                total = topic_dict.get('total_exercises', 0)
                completed = topic_dict.get('completed_exercises', 0)
            elif category == 'math':
                total = topic_dict.get('total_problems', 0)
                completed = topic_dict.get('completed_problems', 0)
            else:
                total = topic_dict.get('total_items', 0)
                completed = topic_dict.get('completed_items', 0)
            
            if total > 0:
                topic_dict['completion_percentage'] = (completed / total) * 100
            else:
                topic_dict['completion_percentage'] = 0
                
            result.append(topic_dict)
            
        return result
    
    @staticmethod
    def update_progress(user_id, topic_id, item_id, item_type='problem', completed=False):
        """Update a user's progress on a specific item"""
        # Check if progress record exists
        existing = query_db(
            """
            SELECT id, completed FROM progress 
            WHERE user_id = ? AND topic_id = ? AND item_id = ? AND item_type = ?
            """,
            [user_id, topic_id, item_id, item_type],
            one=True
        )
        
        if existing:
            # Update existing record
            insert_db(
                """
                UPDATE progress SET completed = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                [1 if completed else 0, existing['id']]
            )
        else:
            # Create new record
            insert_db(
                """
                INSERT INTO progress (user_id, topic_id, item_id, item_type, status, completed)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                [user_id, topic_id, item_id, item_type, 'attempted', 1 if completed else 0]
            )
            
        return True
    
    @staticmethod
    def get_recommended_topics(user_id, category='all'):
        """Get recommended topics for a user based on their progress"""
        # Find topics with low completion percentage in the specified category
        if category != 'all':
            category_filter = f"AND t.category = '{category}'"
        else:
            category_filter = ""
            
        low_completion = query_db(
            f"""
            WITH progress_data AS (
                SELECT t.id, t.name, t.level, t.category, t.subcategory,
                    COALESCE(dsa.total_problems, 0) + 
                    COALESCE(sd.total_exercises, 0) + 
                    COALESCE(math.total_problems, 0) AS total_items,
                    
                    COALESCE(dsa.completed_problems, 0) + 
                    COALESCE(sd.completed_exercises, 0) + 
                    COALESCE(math.completed_problems, 0) AS completed_items
                    
                FROM topics t
                
                LEFT JOIN (
                    SELECT p.topic_id,
                        COUNT(DISTINCT p.id) AS total_problems,
                        COUNT(DISTINCT CASE WHEN pr.completed = 1 THEN p.id END) AS completed_problems
                    FROM problems p
                    LEFT JOIN progress pr ON pr.item_id = p.id AND pr.item_type = 'problem' AND pr.user_id = ?
                    GROUP BY p.topic_id
                ) dsa ON dsa.topic_id = t.id AND t.category = 'dsa'
                
                LEFT JOIN (
                    SELECT e.topic_id,
                        COUNT(DISTINCT e.id) AS total_exercises,
                        COUNT(DISTINCT CASE WHEN pr.completed = 1 THEN e.id END) AS completed_exercises
                    FROM system_design_exercises e
                    LEFT JOIN progress pr ON pr.item_id = e.id AND pr.item_type = 'exercise' AND pr.user_id = ?
                    GROUP BY e.topic_id
                ) sd ON sd.topic_id = t.id AND t.category = 'system_design'
                
                LEFT JOIN (
                    SELECT mp.topic_id,
                        COUNT(DISTINCT mp.id) AS total_problems,
                        COUNT(DISTINCT CASE WHEN pr.completed = 1 THEN mp.id END) AS completed_problems
                    FROM math_problems mp
                    LEFT JOIN progress pr ON pr.item_id = mp.id AND pr.item_type = 'math_problem' AND pr.user_id = ?
                    GROUP BY mp.topic_id
                ) math ON math.topic_id = t.id AND t.category = 'math'
                
                WHERE t.id IN (
                    SELECT DISTINCT topic_id FROM progress WHERE user_id = ?
                ) {category_filter}
            )
            
            SELECT * FROM progress_data
            WHERE total_items > 0
            AND (completed_items * 1.0 / total_items) < 0.5
            ORDER BY (completed_items * 1.0 / total_items), category, level
            LIMIT 5
            """,
            [user_id, user_id, user_id, user_id]
        )
        
        return [dict(topic) for topic in low_completion]
    
    @staticmethod
    def get_user_notes(user_id, topic_id=None):
        """Get a user's notes for a specific topic or all topics"""
        if topic_id:
            notes = query_db(
                """
                SELECT * FROM user_notes
                WHERE user_id = ? AND topic_id = ?
                ORDER BY updated_at DESC
                """,
                [user_id, topic_id]
            )
        else:
            notes = query_db(
                """
                SELECT n.*, t.name as topic_name 
                FROM user_notes n
                JOIN topics t ON n.topic_id = t.id
                WHERE n.user_id = ?
                ORDER BY n.updated_at DESC
                """,
                [user_id]
            )
        
        return [dict(note) for note in notes]
    
    @staticmethod
    def add_user_note(user_id, topic_id, title, content):
        """Add a note for a specific topic"""
        note_id = insert_db(
            """
            INSERT INTO user_notes (user_id, topic_id, title, content)
            VALUES (?, ?, ?, ?)
            """,
            [user_id, topic_id, title, content]
        )
        
        return note_id