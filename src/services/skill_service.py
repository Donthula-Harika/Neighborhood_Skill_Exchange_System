# # from dao.skill_dao import SkillDAO


from dao.skill_dao import SkillDAO

class SkillService:
    def __init__(self):
        self.skill_dao = SkillDAO()

    def add_skill(self, user_id: int, skill_name: str, skill_type: str, category: str):
        if skill_type not in ["Offer", "Request"]:
            raise ValueError("Invalid skill type. Must be 'Offer' or 'Request'.")
        skill = self.skill_dao.add_skill(user_id, skill_name, skill_type, category)
        return skill  # return object; caller (CLI) can format messages

    def view_skills(self, user_id: int):
        """Return all skills of the user."""
        skills = self.skill_dao.get_skills_by_user(user_id)
        return skills

    def update_skill_category(self, skill_id: int, new_category: str):
        """Update the category of a skill."""
        updated_skill = self.skill_dao.update_skill_category(skill_id, new_category)
        return updated_skill

    def list_categories(self):
        """Return all distinct skill categories."""
        return self.skill_dao.list_categories()

    def get_skills_by_category(self, category_name: str):
        """Return all skills in a specific category."""
        return self.skill_dao.get_skills_by_category(category_name)