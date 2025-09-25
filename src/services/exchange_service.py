#  src/services/exchange_service.py


from dao.exchange_dao import ExchangeDAO

class ExchangeService:
    def __init__(self):
        self.exchange_dao = ExchangeDAO()

    def request_exchange(self, requester_id: int, responder_id: int, 
                         skill_offered: str, skill_requested: str, 
                         scheduled_time=None):
        """Create a new skill exchange request."""
        if requester_id == responder_id:
            raise ValueError("Requester and responder cannot be the same user.")
        return self.exchange_dao.create_exchange(
            requester_id, responder_id, skill_offered, skill_requested, scheduled_time
        )

    def complete_exchange(self, exchange_id: int):
        """Mark an exchange as completed."""
        return self.exchange_dao.update_exchange_status(exchange_id, "Completed")

    def get_exchange_details(self, exchange_id: int):
        """Fetch details of a specific exchange."""
        return self.exchange_dao.get_exchange_by_id(exchange_id)

    def list_all_exchanges(self):
        """List all skill exchanges in the system."""
        return self.exchange_dao.list_exchanges()

    def get_exchanges_for_user(self, user_id: int):
        """List all exchanges where the user is either the requester or the responder."""
        try:
            return self.exchange_dao.get_exchanges_for_user(user_id)
        except Exception as e:
            # return None or raise depending on how you want to handle it. Keeping return message for CLI compatibility.
            return f"Error fetching exchanges: {e}"
    
    def respond_to_exchange(self, exchange_id: int, accept: bool):
        """Only allow responding if status is Pending"""
        exchange = self.exchange_dao.get_exchange_by_id(exchange_id)
        if not exchange:
            return "Exchange not found."
        if exchange.get("status") != "Pending":
            return f"Cannot respond, current status is {exchange.get('status')}."
        status = "Accepted" if accept else "Rejected"
        return self.exchange_dao.update_exchange_status(exchange_id, status)
