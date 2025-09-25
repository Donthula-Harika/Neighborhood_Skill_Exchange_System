# from dao.feedback_dao import FeedbackDAO



from dao.feedback_dao import FeedbackDAO
from dao.exchange_dao import ExchangeDAO

class FeedbackService:
    def __init__(self):
        self.feedback_dao = FeedbackDAO()
        self.exchange_dao = ExchangeDAO()

    def add_feedback(self, user_id, exchange_id, rating, comments, user_service=None):
        """
        Add feedback and optionally update the recipient's reputation.
        We derive the recipient from the exchange (requester/responder).
        """
        exchange = self.exchange_dao.get_exchange_by_id(exchange_id)
        if not exchange:
            raise ValueError("Exchange not found.")

        # Determine recipient (the other participant)
        recipient_id = exchange["responder_id"] if exchange["responder_id"] != user_id else exchange["requester_id"]

        feedback = self.feedback_dao.create_feedback(user_id, exchange_id, rating, comments, recipient_id=recipient_id)

        if feedback and user_service:
            # Update reputation points of the recipient
            user_service.update_reputation(recipient_id, rating)

        return feedback

    def get_feedback_for_exchange(self, exchange_id):
        """Get feedback for a specific exchange"""
        return self.feedback_dao.get_feedback_by_exchange(exchange_id)

    def get_feedback_for_user(self, user_id):
        """Get all feedback received by a user"""
        return self.feedback_dao.list_feedback_for_user(user_id)
