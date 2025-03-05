from pydantic import BaseModel

import os
from dotenv import load_dotenv

class Settings(BaseModel):
    load_dotenv()

    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    ALGORITHM: str = os.getenv("ALGORITHM")

    class Config:
        env_file = ".env"

settings = Settings()