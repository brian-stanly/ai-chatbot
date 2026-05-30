from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str
    DEBUG: bool
    DATABASE_URL: str
    GROK_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
