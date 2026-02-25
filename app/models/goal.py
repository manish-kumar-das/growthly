"""
Goal Model
"""

class Goal:
    """Goal model class"""
    
    def __init__(self, id=None, habit_id=None, goal_type=None, target_value=0, 
                 current_value=0, is_completed=False, created_at=None, completed_at=None):
        self.id = id
        self.habit_id = habit_id
        self.goal_type = goal_type
        self.target_value = target_value
        self.current_value = current_value
        self.is_completed = is_completed
        self.created_at = created_at
        self.completed_at = completed_at
    
    def __repr__(self):
        return f"Goal(id={self.id}, habit_id={self.habit_id}, type={self.goal_type})"