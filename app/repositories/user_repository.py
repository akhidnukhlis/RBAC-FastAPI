from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.schemas import user_schema
from app.models import user_model
from app.core.security import security_manager


class UsersRepository:
    def __init__(self, db: Session):
        """
        Inisialisasi class dengan session database.
        """
        self.db = db

    def create_user(self, user: user_schema.UserCreate) -> user_model.User:
        """
        Membuat user baru di database dengan password yang sudah di-hash.
        """
        hashed_password = security_manager.hash_password(user.password)
        db_user = user_model.User(
            email=str(user.email),
            hashed_password=hashed_password,
            role_id=user.role_id,
            is_active=user.is_active
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_users(self) -> List[user_model.User]:
        """
        Mengambil daftar semua user beserta status dan role mereka.
        """
        return self.db.query(user_model.User).options(
            joinedload(user_model.User.role),
            joinedload(user_model.User.status)
        )

    def get_user_by_email(self, email: str) -> Optional[user_model.User]:
        """
        Mencari user berdasarkan email.
        """
        return self.db.query(user_model.User).options(
            joinedload(user_model.User.role),
            joinedload(user_model.User.status)
        ).filter(user_model.User.email == email).first()

    def update_user(self, user_id: str, user: user_schema.UserUpdate) -> Optional[user_model.User]:
        """
        Memperbarui data user (role, status, active state).
        """
        db_user = self.db.query(user_model.User).filter(user_model.User.id == user_id).first()
        if not db_user:
            return None

        if user.role_id is not None:
            db_user.role_id = user.role_id
        if user.status_id is not None:
            db_user.status_id = user.status_id
        if user.is_active is not None:
            db_user.is_active = user.is_active

        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: str) -> bool:
        """
        Menghapus user secara permanen.
        """
        db_user = self.db.query(user_model.User).filter(user_model.User.id == user_id).first()
        if not db_user:
            return False

        self.db.delete(db_user)
        self.db.commit()
        return True

    def authenticate_user(self, email: str, password: str) -> Optional[user_model.User]:
        """
        Memverifikasi kredensial user (email & password).
        """
        # 1. Cari user berdasarkan email
        user = self.get_user_by_email(email)
        if user is None:
            return None
            
        # 2. Validasi tambahan: pastikan email yang dikembalikan benar-benar cocok (case-sensitive jika perlu)
        if user.email != email:
             return None

        # 3. Pastikan password hash ada
        if not user.hashed_password:
            return None

        # 4. Verifikasi password
        try:
            is_valid = security_manager.verify_password(password, str(user.hashed_password))
            if not is_valid:
                return None
        except Exception:
            # Jika verify_password error (misal format hash salah), anggap gagal
            return None
            
        return user

    def get_user_by_access_token(self, token: str) -> Optional[user_model.User]:
        """
        Mencari user berdasarkan access token yang aktif.
        """
        return self.db.query(user_model.User).filter(
            user_model.User.access_token == token,
            user_model.User.is_active == True
        ).first()

    def update_user_token(self, user_id: str, token: str) -> Optional[user_model.User]:
        """
        Menyimpan token akses terbaru ke data user.
        """
        user = self.db.query(user_model.User).filter(user_model.User.id == user_id).first()
        if user:
            user.access_token = token
            self.db.commit()
            self.db.refresh(user)
        return user