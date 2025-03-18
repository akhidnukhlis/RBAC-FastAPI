from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import UserCreate, UserUpdate, UserResponse
from app.core.database import get_db
from app.services import users as user_service
from app.middleware.permission_middleware import PermissionMiddleware
from app.middleware.auth_middleware import AuthMiddleware

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", dependencies=[Depends(AuthMiddleware), Depends(PermissionMiddleware(2))], response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return user_service.list_users(db)

@router.post("/", dependencies=[Depends(AuthMiddleware), Depends(PermissionMiddleware(1))], response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.register_user(db, user)

@router.put("/{id}", dependencies=[Depends(AuthMiddleware), Depends(PermissionMiddleware(3))], response_model=UserResponse)
def update_user(id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return user_service.modify_user(db, id, user)

@router.delete("/{id}", dependencies=[Depends(AuthMiddleware), Depends(PermissionMiddleware(6))])
def delete_user(id: int, db: Session = Depends(get_db)):
    return user_service.remove_user(db, id)


