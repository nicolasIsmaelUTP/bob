from supabase import create_client, Client
from .config import Config

class SupabaseClient:
    _instance: Client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = create_client(
                Config.SUPABASE_URL,
                Config.SUPABASE_SERVICE_ROLE
            )
        return cls._instance

def get_supabase_client() -> Client:
    return SupabaseClient()
