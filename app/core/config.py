from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Fraud Detection API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str
    API_KEY: str

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()