from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    SECRET_KEY: str = "dev_jwt_secret_key_change_in_production_32bytes"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    # Database URLs
    DATABASE_URL: str = "postgresql+asyncpg://therados:therados_dev_password@localhost:5432/therados_db"
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "therados_dev_password"
    REDIS_URL: str = "redis://localhost:6379/0"

    # Object Storage
    S3_ENDPOINT_URL: Optional[str] = "http://localhost:9000"
    S3_ACCESS_KEY: Optional[str] = "therados_minio"
    S3_SECRET_KEY: Optional[str] = "therados_dev_password"
    S3_BUCKET_NAME: str = "therados-files"

    # Workflow Orchestration
    TEMPORAL_HOST: str = "localhost:7233"

    # Model Fabric Keys
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None

    # Tools
    AUTODOCK_VINA_PATH: Optional[str] = None

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
