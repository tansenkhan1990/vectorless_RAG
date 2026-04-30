# Supabase Database Connection
# Initializes and manages connection to Supabase PostgreSQL database

from supabase import create_client
from app.config.settings import settings

# Initialize Supabase client
# This client is used for all database operations (insert, select, RPC calls, etc.)
supabase = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_KEY
)

# Verify connection on import
try:
    # Test connection with a simple query
    test = supabase.table("documents").select("*", count="exact").limit(1).execute()
    print(f"✓ Connected to Supabase - Found {test.count or 0} documents")
except Exception as e:
    print(f"⚠️  Supabase connection error: {e}")
