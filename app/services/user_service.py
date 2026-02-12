import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Optional, Dict

from app.core.security import security_manager
from app.core.config import settings
from app.repositories import user_repository
from app.schemas import user_schema

class UserService:
    def __init__(self, db: Session):
        """
        Inisialisasi Service dengan session database.
        """
        self.db = db
        self.repo = user_repository.UsersRepository(db)

    def register(self, user_data: user_schema.UserCreate):
        """Mendaftarkan user baru dengan validasi email dan username."""
        # Cek email
        if self.repo.get_user_by_email(str(user_data.email)):
            raise HTTPException(status_code=400, detail="Email already exists")

        return self.repo.create_user(user_data)

    def login(self, login_data: user_schema.UserLogin) -> Optional[Dict[str, str]]:
        """Proses autentikasi dan pembuatan token."""
        # Validasi: Cek apakah email terdaftar
        user_exists = self.repo.get_user_by_email(login_data.email)
        if not user_exists:
            raise HTTPException(status_code=400, detail="Email is not registered")

        authenticated_user = self.repo.authenticate_user(
            login_data.email, login_data.password
        )

        # Validasi user dan password (double check for safety)
        if not authenticated_user:
            return None

        # Siapkan payload JWT
        payload = {
            "user_id": authenticated_user.id,
            "role_id": authenticated_user.role_id,
            "status_id": authenticated_user.status_id,
            "email": authenticated_user.email
        }

        expires_delta = datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token = security_manager.create_access_token(payload, expires_delta)

        # Update token di database (session management)
        self.repo.update_user_token(authenticated_user.id, token)

        return {"access_token": token, "token_type": "bearer"}

    def list_all(self):
        """Mendapatkan semua daftar user."""
        return self.repo.get_users()

    def update(self, user_id: str, user_data: user_schema.UserUpdate):
        """Mengubah data user dan validasi keberadaannya."""
        updated_user = self.repo.update_user(
            user_id=user_id, user=user_data
        )
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")

        return updated_user

    def delete(self, user_id: str) -> Dict[str, str]:
        """Menghapus user dan validasi keberadaannya."""
        success = self.repo.delete_user(user_id=user_id)
        if not success:
            raise HTTPException(status_code=404, detail="User not found")

        return {"message": "User deleted successfully"}