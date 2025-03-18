from pydantic import BaseModel
import os
from dotenv import load_dotenv

class Settings(BaseModel):
    load_dotenv()

    # DATABASE CONFIG
    db_host: str = os.getenv("POSTGRES_HOST", "localhost")
    db_user: str = os.getenv("POSTGRES_USER", "user")
    db_password: str = os.getenv("POSTGRES_PASSWORD", "password")
    db_name: str = os.getenv("POSTGRES_DB", "database")
    db_port: int = int(os.getenv("POSTGRES_PORT", 5432))

    # JWT CONFIG
    SECRET_KEY: str = os.getenv("SECRET_KEY", "secret")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    class Config:
        env_file = ".env"

settings = Settings()
