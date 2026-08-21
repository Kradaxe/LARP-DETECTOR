from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str = ""
    GITHUB_TOKEN: str = ""
    DATABASE_URL: str = "postgresql+psycopg://larp_user:larp_password@localhost:5432/larp_detector"

    class Config:
        env_file = ".env"


settings = Settings()
