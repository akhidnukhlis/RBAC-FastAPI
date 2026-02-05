from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any

from app.core.database import db_manager  # Menggunakan DatabaseManager class
from app.services.user_service import UserService  # Menggunakan UserService class
from app.schemas.user_schema import UserLogin, UserRegister, UserCreate, UserResponse

router = APIRouter(tags=["Auth"])


# Helper untuk inisialisasi UserService
def get_user_service(db: Session = Depends(db_manager.get_db)) -> UserService:
    return UserService(db)


@router.post("/register", response_model=UserResponse, response_model_exclude_none=True)
def register(
        user_data: UserRegister,
        service: UserService = Depends(get_user_service)
):
    """
    Endpoint untuk registrasi. Validasi email/username sudah ditangani
    di dalam service.register().
    """
    # Konversi dari UserRegister ke UserCreate (jika diperlukan oleh service)
    user_create = UserCreate(
        email=user_data.email,
        password=user_data.password,
        is_active=False
    )

    return service.register(user_create)


@router.post("/login")
def login(
        login_data: UserLogin,
        service: UserService = Depends(get_user_service)
) -> Any:
    """
    Endpoint login. Menghasilkan token JWT jika kredensial valid.
    """
    token_response = service.login(login_data)

    if not token_response:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return token_response