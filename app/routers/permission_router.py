from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate
from app.utils.pagination import CustomPage as Page

from app.schemas import permission_schema
from app.core.database import db_manager as DBManager
from app.services.permission_service import PermissionService
from app.middleware.permission_middleware import PermissionMiddleware
from app.middleware.auth_middleware import auth_handler

router = APIRouter(prefix="/permissions", tags=["Permissions"])

# Helper untuk inisialisasi service
def get_permission_service(db: Session = Depends(DBManager.get_db)):
    return PermissionService(db)

@router.get("/", 
    dependencies=[Depends(auth_handler), Depends(PermissionMiddleware(2))], 
    response_model=Page[permission_schema.PermissionResponse])
def list_permissions(service: PermissionService = Depends(get_permission_service)):
    """
    Mendapatkan daftar permission dengan pagination.
    Requires: Permission:Read (Level 2)
    """
    return paginate(service.list_all())

@router.get("/{id}", 
    dependencies=[Depends(auth_handler), Depends(PermissionMiddleware(2))], 
    response_model=permission_schema.PermissionResponse)
def get_permission(id: int, service: PermissionService = Depends(get_permission_service)):
    """
    Mendapatkan detail permission berdasarkan ID.
    Requires: Permission:Read (Level 2)
    """
    return service.get_by_id(id)

@router.post("/", 
    dependencies=[Depends(auth_handler), Depends(PermissionMiddleware(1))], 
    response_model=permission_schema.PermissionResponse)
def create_permission(permission: permission_schema.PermissionCreate, service: PermissionService = Depends(get_permission_service)):
    """
    Membuat permission baru.
    Requires: Permission:Create (Level 1)
    """
    return service.create(permission)

@router.put("/{id}", 
    dependencies=[Depends(auth_handler), Depends(PermissionMiddleware(3))], 
    response_model=permission_schema.PermissionResponse)
def update_permission(id: int, permission: permission_schema.PermissionUpdate, service: PermissionService = Depends(get_permission_service)):
    """
    Mengupdate permission yang sudah ada.
    Requires: Permission:Update (Level 3)
    """
    return service.update(id, permission)

@router.delete("/{id}", 
    dependencies=[Depends(auth_handler), Depends(PermissionMiddleware(6))]) 
def delete_permission(id: int, service: PermissionService = Depends(get_permission_service)):
    """
    Menghapus permission berdasarkan ID.
    Requires: Permission:Delete (Level 6)
    """
    return service.delete(id)
