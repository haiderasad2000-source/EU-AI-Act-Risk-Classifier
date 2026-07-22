from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./ai_risk_assessments.db"
    draft_version: str = "EU-AI-Act-v1.1"
    use_mock_classifier: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
