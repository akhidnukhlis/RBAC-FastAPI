from pydantic import BaseModel
import os
from dotenv import load_dotenv
from typing import List

class Settings(BaseModel):
    load_dotenv()

    # DATABASE CONFIG
    # os.getenv tanpa argumen kedua akan menghasilkan None jika key tidak ditemukan
    db_host: str = os.getenv("POSTGRES_HOST")
    db_user: str = os.getenv("POSTGRES_USER")
    db_password: str = os.getenv("POSTGRES_PASSWORD")
    db_name: str = os.getenv("POSTGRES_DB")
    
    # Untuk tipe data int, perlu menangani potensi nilai None agar tidak error saat casting
    db_port_raw: str = os.getenv("POSTGRES_PORT")
    db_port: int = int(db_port_raw) if db_port_raw else 0

    # JWT CONFIG
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    
    expire_minutes_raw: str = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(expire_minutes_raw) if expire_minutes_raw else 0

    # CORS CONFIG
    frontend_url: str = os.getenv("FRONTEND_URL")

    @property
    def DATABASE_URL(self) -> str:
        # Pengecekan manual untuk memastikan semua variabel wajib ada
        if not all([self.db_user, self.db_password, self.db_host, self.db_name]):
            raise ValueError("Database configuration is incomplete in .env file")
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def cors_origins(self) -> List[str]:
        if not self.frontend_url:
            return []
        return [url.strip() for url in self.frontend_url.split(",")]

    class Config:
        env_file = ".env"

settings = Settings()