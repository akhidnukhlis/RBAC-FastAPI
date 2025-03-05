import datetime

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.core import security
from app.core.config import settings
from app.repositories import user as user_repository
from app.schemas.user import UserCreate, UserLogin, UserUpdate


def register_user(db: Session, user: UserCreate):
    is_email_existed = user_repository.get_user_by_email(db, str(user.email))
    if is_email_existed:
        raise HTTPException(status_code=400, detail="Email already exists")

    is_username_existed = user_repository.get_user_by_username(db, str(user.username))
    if is_username_existed:
        raise HTTPException(status_code=400, detail="Username already exists")

    return user_repository.create_user(db, user)

def login_user(db: Session, user: UserLogin):
    authenticated_user = user_repository.authenticate_user(db, user.username, user.password)

    if not authenticated_user or not security.verify_password(user.password, authenticated_user.hashed_password):
        return None

    payload = {
        "user_id": authenticated_user.id,
        "role_id": authenticated_user.role_id,
        "status_id": authenticated_user.status_id,
        "email": authenticated_user.email
    }

    expires_delta = datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    token = security.create_access_token(payload, expires_delta)

    user_repository.update_user_token(db, authenticated_user.id, token)

    return {"access_token": token, "token_type": "bearer"}

def list_users(db: Session):
    return user_repository.get_users(db)

def modify_user(db: Session, user_id: int, user: UserUpdate):
    updated_user = user_repository.update_user(db=db, user_id=user_id, user=user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")

    return updated_user

def remove_user(db: Session, user_id: int):
    success = user_repository.delete_user(db=db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted"}
