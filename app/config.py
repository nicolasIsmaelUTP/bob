from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    VERSION: str
    PHONE_NUMBER_ID: str
    RECIPIENT_PHONE_NUMBER: str
    ACCESS_TOKEN: str
    

    model_config = SettingsConfigDict(
            env_file=".env",
            extra="ignore"
        )

Config = Settings()