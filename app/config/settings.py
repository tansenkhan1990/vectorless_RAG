import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MODEL = os.getenv("LOCAL_MODEL_NAME")
    BASE_URL = os.getenv("OPENAI_BASE_URL")
    API_KEY = os.getenv("OPENAI_API_KEY")

    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

settings = Settings()