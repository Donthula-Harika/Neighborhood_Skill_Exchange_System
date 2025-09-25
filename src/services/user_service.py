#  src/services/user_service.py


from dao.user_dao import UserDAO

class UserService:
    def __init__(self):
        self.user_dao = UserDAO()

    def register_user(self, name: str, email: str, password: str):
        """Register a new user."""
        return self.user_dao.create_user(name, email, password)

    def login_user(self, email: str, password: str):
        """Login an existing user."""
        return self.user_dao.login_user(email, password)

    def get_user_by_id(self, user_id: int):
        """Fetch a user by their ID."""
        return self.user_dao.get_user_by_id(user_id)

    def update_reputation(self, user_id: int, points: int):
        """Update a user's reputation points."""
        return self.user_dao.update_reputation(user_id, points)

    def list_all_users(self):
        """Return all users in the system."""
        users = self.user_dao.list_users()
        return users
