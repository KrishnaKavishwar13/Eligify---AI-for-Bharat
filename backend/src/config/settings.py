"""Application configuration settings"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # AWS Configuration
    AWS_REGION: str = "us-east-1"
    AWS_ACCOUNT_ID: str = ""

    # DynamoDB Tables
    DYNAMODB_STUDENTS_TABLE: str = "eligify-students"
    DYNAMODB_SKILLS_TABLE: str = "eligify-skills"
    DYNAMODB_INTERNSHIPS_TABLE: str = "eligify-internships"
    DYNAMODB_PROJECTS_TABLE: str = "eligify-projects"
    DYNAMODB_VALIDATIONS_TABLE: str = "eligify-validations"

    # S3 Buckets
    S3_RESUME_BUCKET: str = "eligify-resumes"

    # Cognito
    COGNITO_USER_POOL_ID: str = ""
    COGNITO_CLIENT_ID: str = ""

    # JWT
    JWT_SECRET: str = "change-me-in-production"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    JWT_ALGORITHM: str = "HS256"

    # AI Services
    BEDROCK_MODEL_ID: str = "anthropic.claude-3-sonnet-20240229-v1:0"
    OPENAI_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    # API Configuration
    API_BASE_URL: str = "http://localhost:8000"
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001"]

    # Environment
    ENVIRONMENT: str = "development"


# Global settings instance
settings = Settings()
