from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    VERSION: str
    PHONE_NUMBER_ID: str
    RECIPIENT_PHONE_NUMBER: str
    ACCESS_TOKEN: str
    OPENAI_API_KEY: str
    SUPABASE_URL: str
    SUPABASE_SERVICE_ROLE: str
    # SUPABASE_PASSWORD: str

    model_config = SettingsConfigDict(
            env_file=Path(__file__).parent / ".env",
            extra="ignore"
        )

Config = Settings()