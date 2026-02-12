from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import role_schema
from app.core.database import db_manager as DBManager
from app.services.role_service import RoleService
from app.middleware.permission_middleware import PermissionMiddleware
from app.middleware.auth_middleware import auth_handler
from fastapi_pagination.ext.sqlalchemy import paginate
from app.utils.pagination import CustomPage as Page

router = APIRouter(prefix="/roles", tags=["Roles"])

# Helper untuk inisialisasi service
def get_role_service(db: Session = Depends(DBManager.get_db)):
    return RoleService(db)

@router.get("/", 
    dependencies=[Depends(auth_handler), Depends(PermissionMiddleware(2))], # Menggunakan permission level yang sama dengan user list sementara
    response_model=Page[role_schema.RoleResponse])
def list_roles(service: RoleService = Depends(get_role_service)):
    """
    Daftar semua role.
    Requires: Role:Read (Level 2)
    """
    return paginate(service.list_all())

@router.get("/{id}", 
    dependencies=[Depends(auth_handler), Depends(PermissionMiddleware(2))], 
    response_model=role_schema.RoleResponse)
def get_role(id: int, service: RoleService = Depends(get_role_service)):
    """
    Detail role by ID.
    Requires: Role:Read (Level 2)
    """
    return service.get_by_id(id)

@router.post("/", 
    dependencies=[Depends(auth_handler), Depends(PermissionMiddleware(1))], # Menggunakan permission level create user sementara
    response_model=role_schema.RoleResponse)
def create_role(role: role_schema.RoleCreate, service: RoleService = Depends(get_role_service)):
    """
    Membuat role baru.
    Requires: Role:Create (Level 1)
    """
    return service.create(role)

@router.put("/{id}", 
    dependencies=[Depends(auth_handler), Depends(PermissionMiddleware(3))], # Menggunakan permission level update user sementara
    response_model=role_schema.RoleResponse)
def update_role(id: int, role: role_schema.RoleUpdate, service: RoleService = Depends(get_role_service)):
    """
    Update role.
    Requires: Role:Update (Level 3)
    """
    return service.update(id, role)

@router.delete("/{id}", 
    dependencies=[Depends(auth_handler), Depends(PermissionMiddleware(6))]) # Menggunakan permission level delete user sementara
def delete_role(id: int, service: RoleService = Depends(get_role_service)):
    """
    Hapus role.
    Requires: Role:Delete (Level 6)
    """
    return service.delete(id)
