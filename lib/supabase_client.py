"""Supabase client for PeterOS Calgary MediSpa AI."""
import os
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("NEXT_PUBLIC_SUPABASE_URL", "")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
SUPABASE_ANON_KEY = os.environ.get("NEXT_PUBLIC_SUPABASE_ANON_KEY", "")

def get_admin_client() -> Client:
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set")
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

def get_anon_client() -> Client:
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set")
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def test_connection() -> dict:
    try:
        client = get_admin_client()
        result = client.table("system_config").select("config_key").limit(1).execute()
        return {"status": "connected", "rows": len(result.data)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    print(test_connection())
