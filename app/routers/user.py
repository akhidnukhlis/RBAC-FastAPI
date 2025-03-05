from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import UserCreate, UserUpdate, UserResponse
from app.core.database import get_db
from app.services import user as user_service

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return user_service.list_users(db)

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.register_user(db, user)

@router.put("/{id}", response_model=UserResponse)
def update_user(id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return user_service.modify_user(db, id, user)

@router.delete("/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    return user_service.remove_user(db, id)


