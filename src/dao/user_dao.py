
        
        
# src/dao/user_dao.py
from config import supabase
import bcrypt

class UserDAO:
    def __init__(self):
        self.table = supabase.from_("users")

    def create_user(self, name: str, email: str, password: str):
        """Register a new user with hashed password"""
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        data = {
            "name": name,
            "email": email,
            "password": hashed_pw,
            "reputation_points": 0
        }
        response = self.table.insert(data).execute()
        if getattr(response, 'error', None):
            raise Exception(f"Failed to create user: {response.error}")
        return response.data[0] if response.data else None

    def login_user(self, email: str, password: str):
        """Login user with email and hashed password check"""
        response = self.table.select("*").eq("email", email).execute()
        if response.data:
            user = response.data[0]
            if bcrypt.checkpw(password.encode(), user["password"].encode()):
                return user
        return None

    def get_user_by_id(self, user_id: int):
        response = self.table.select("*").eq("user_id", user_id).execute()
        return response.data[0] if response.data else None

    def update_reputation(self, user_id: int, points: int):
        user = self.get_user_by_id(user_id)
        if user:
            new_points = user["reputation_points"] + points
            response = self.table.update({"reputation_points": new_points}).eq("user_id", user_id).execute()
            return response.data[0] if response.data else None
        return None

    
    def list_users(self):
        """Return all users."""
        response = self.table.select("*").execute()
        return response.data if response.data else []



