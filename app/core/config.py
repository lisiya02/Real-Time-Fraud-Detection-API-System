from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Fraud Detection API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # Database configuration (also used directly by docker-compose.yml)
    DATABASE_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    class Config:
        env_file = ".env"


settings = Settings()