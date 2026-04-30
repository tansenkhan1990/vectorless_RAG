# Configuration Settings
# Loads environment variables and provides application configuration

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """
    Application configuration loaded from environment variables.
    
    Attributes:
        MODEL (str): LLM model identifier (e.g., "qwen3-vl:235b-cloud")
        BASE_URL (str): LLM API base URL (e.g., "http://localhost:11434/v1")
        API_KEY (str): LLM API authentication key
        SUPABASE_URL (str): Supabase project URL
        SUPABASE_KEY (str): Supabase publishable API key
    """
    
    # LLM Configuration
    MODEL = os.getenv("LOCAL_MODEL_NAME")
    BASE_URL = os.getenv("OPENAI_BASE_URL")
    API_KEY = os.getenv("OPENAI_API_KEY")

    # Supabase Configuration
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    
    @classmethod
    def validate(cls):
        """Validate that all required settings are configured."""
        required = ["MODEL", "BASE_URL", "API_KEY", "SUPABASE_URL", "SUPABASE_KEY"]
        missing = [attr for attr in required if not getattr(cls, attr)]
        
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")


# Create settings instance
settings = Settings()

# Optionally validate on import
try:
    settings.validate()
except ValueError as e:
    print(f"⚠️  Warning: {e}")
