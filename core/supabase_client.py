import os
from supabase import create_client, Client
import environ

# Re-init Env in case it's needed outside Django's context
env = environ.Env()
environ.Env.read_env(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

def get_supabase() -> Client:
    """
    Get a configured Supabase client.
    Requires SUPABASE_URL and SUPABASE_KEY in your .env
    """
    url: str = os.environ.get("SUPABASE_URL", "")
    key: str = os.environ.get("SUPABASE_KEY", "")
    
    if not url or not key:
        print("Warning: Supabase credentials not found in env.")
        return None
        
    return create_client(url, key)

# Create a singleton instance for convenience
supabase = get_supabase()
