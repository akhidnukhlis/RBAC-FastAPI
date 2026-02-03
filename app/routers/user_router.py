from fastapi import APIRouter, Depends
from fastapi_pagination import paginate
from app.utils.pagination import CustomPage as Page
from sqlalchemy.orm import Session
from app.schemas import user_schema 
from app.core.database import db_manager as DBManager # Menggunakan class DatabaseManager kita
from app.services.user_service import UserService # Menggunakan class UserService kita
from app.middleware.permission_middleware import PermissionMiddleware
from app.middleware.auth_middleware import auth_handler # Menggunakan class AuthService kita

router = APIRouter(prefix="/users", tags=["Users"])

# Helper untuk inisialisasi service
def get_user_service(db: Session = Depends(DBManager.get_db)):
    return UserService(db)

@router.get("/", 
    dependencies=[Depends(auth_handler), Depends(PermissionMiddleware(2))], 
    response_model=Page[user_schema.UserResponse])
def list_users(service: UserService = Depends(get_user_service)):
    return paginate(service.list_all())

@router.post("/", 
    dependencies=[Depends(auth_handler), Depends(PermissionMiddleware(1))], 
    response_model=user_schema.UserResponse)
def create_user(user: user_schema.UserCreate, service: UserService = Depends(get_user_service)):
    return service.register(user)

@router.put("/{id}", 
    dependencies=[Depends(auth_handler), Depends(PermissionMiddleware(3))], 
    response_model=user_schema.UserResponse)
def update_user(id: str, user: user_schema.UserUpdate, service: UserService = Depends(get_user_service)):
    return service.update(id, user)

@router.delete("/{id}", 
    dependencies=[Depends(auth_handler), Depends(PermissionMiddleware(6))])
def delete_user(id: str, service: UserService = Depends(get_user_service)):
    return service.delete(id)