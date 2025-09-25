
# src/dao/skill_dao.py
from config import supabase

class SkillDAO:
    def __init__(self):
        self.table = supabase.from_("skills")

    def add_skill(self, user_id: int, skill_name: str, skill_type: str, category: str):
        data = {
            "user_id": user_id,
            "skill_name": skill_name,
            "skill_type": skill_type,
            "category": category
        }
        response = self.table.insert(data).execute()
        if getattr(response, 'error', None):
            raise Exception(f"Failed to add skill: {response.error}")
        return response.data[0] if response.data else None

    def get_skills_by_user(self, user_id: int):
        response = self.table.select("*").eq("user_id", user_id).execute()
        return response.data if response.data else []

    def update_skill_category(self, skill_id: int, new_category: str):
        response = self.table.update({"category": new_category}).eq("skill_id", skill_id).execute()
        if getattr(response, 'error', None):
            raise Exception(f"Failed to update category: {response.error}")
        return response.data[0] if response.data else None

    def search_skills(self, skill_type=None, category=None):
        query = self.table.select("*")
        if skill_type:
            query = query.eq("skill_type", skill_type)
        if category:
            query = query.eq("category", category)
        response = query.execute()
        return response.data if response.data else []


    def get_skills_by_category(self, category_name: str):
        """Return all skills under a given category."""
        response = self.table.select("*").eq("category", category_name).execute()
        return response.data if response.data else []

    def list_categories(self):
        """Return distinct categories of all skills."""
        response = self.table.select("category").execute()
        categories = list({r["category"] for r in response.data}) if response.data else []
        return categories