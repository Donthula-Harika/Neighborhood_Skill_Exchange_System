# src/dao/exchange_dao.py
from config import supabase

class ExchangeDAO:
    def __init__(self):
        self.table = supabase.from_("exchanges")

    def create_exchange(self, requester_id: int, responder_id: int, skill_offered: str, skill_requested: str, scheduled_time=None):
        data = {
            "requester_id": requester_id,
            "responder_id": responder_id,
            "skill_offered": skill_offered,
            "skill_requested": skill_requested,
            "status": "Pending",
            "scheduled_time": scheduled_time
        }
        response = self.table.insert(data).execute()
        if getattr(response, 'error', None):
            raise Exception(f"Failed to create exchange: {response.error}")
        return response.data[0] if response.data else None

    def update_exchange_status(self, exchange_id: int, status: str):
        response = self.table.update({"status": status}).eq("exchange_id", exchange_id).execute()
        if getattr(response, 'error', None):
            raise Exception(f"Failed to update status: {response.error}")
        return response.data[0] if response.data else None

    def get_exchange_by_id(self, exchange_id: int):
        response = self.table.select("*").eq("exchange_id", exchange_id).execute()
        return response.data[0] if response.data else None

    def list_exchanges(self):
        response = self.table.select("*").execute()
        return response.data if response.data else []

    def get_exchanges_for_user(self, user_id: int):
        """Fetch all exchanges involving a specific user"""
        response = self.table.select("*").or_(f"requester_id.eq.{user_id},responder_id.eq.{user_id}").execute()
        return response.data if response.data else []
