# src/dao/feedback_dao.py

from config import supabase

class FeedbackDAO:
    def __init__(self):
        self.table = supabase.from_("feedback")

    def create_feedback(self, user_id, exchange_id, rating, comments, recipient_id=None):
        """
        Create feedback.
        - user_id: who gave the feedback
        - recipient_id: who received the feedback (optional; service should set it)
        """
        data = {
            "user_id": user_id,
            "exchange_id": exchange_id,
            "rating": rating,
            "comments": comments
        }
        if recipient_id is not None:
            data["recipient_id"] = recipient_id

        response = self.table.insert(data).execute()
        if getattr(response, 'error', None):
            raise Exception(f"Failed to add feedback: {response.error}")
        return response.data[0] if response.data else None

    def get_feedback_by_exchange(self, exchange_id):
        response = self.table.select("*").eq("exchange_id", exchange_id).execute()
        return response.data if response.data else []

    def list_feedback_for_user(self, user_id):
        """Return feedback *about* a user (i.e., where recipient_id == user_id)."""
        response = self.table.select("*").eq("recipient_id", user_id).execute()
        return response.data if response.data else []

    def get_average_rating_for_user(self, user_id):
        """Compute average rating *received* by a user."""
        response = self.table.select("rating").eq("recipient_id", user_id).execute()
        ratings = [r["rating"] for r in response.data] if response.data else []
        return sum(ratings)/len(ratings) if ratings else 0
