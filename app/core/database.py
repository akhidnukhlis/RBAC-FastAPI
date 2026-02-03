from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from app.core.config import settings

class DatabaseManager:
    def __init__(self, db_url: str = settings.DATABASE_URL):
        # 1. Setup Engine
        self.engine = create_engine(
            db_url,
            # pool_pre_ping=True sering ditambahkan untuk menjaga koneksi tetap hidup
            pool_pre_ping=True 
        )
        
        # 2. Setup Session Factory
        self.SessionLocal = sessionmaker(
            bind=self.engine, 
            autocommit=False, 
            autoflush=False
        )
        
        # 3. Base untuk Model SQLAlchemy
        self.Base = declarative_base()

    def get_db(self) -> Generator[Session, None, None]:
        """
        Generator function untuk menyediakan session database.
        Digunakan sebagai dependency di FastAPI.
        """
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def create_tables(self):
        """
        Membuat semua tabel yang terdaftar di Base.
        Biasanya dipanggil saat aplikasi startup.
        """
        self.Base.metadata.create_all(bind=self.engine)

# Inisialisasi instance tunggal
db_manager = DatabaseManager()

# Shortcut untuk Base agar mudah diimport di file models.py
Base = db_manager.Base