from pydantic_settings import BaseSettings , SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET : str
    JWT_ALGO: str
    REDIS_HOST :str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Load config
Config = Settings()