from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi_pagination import paginate
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
    return paginate(service.list_all())

@router.get("/{id}", 
    dependencies=[Depends(auth_handler), Depends(PermissionMiddleware(2))], 
    response_model=permission_schema.PermissionResponse)
def get_permission(id: int, service: PermissionService = Depends(get_permission_service)):
    return service.get_by_id(id)

@router.post("/", 
    dependencies=[Depends(auth_handler), Depends(PermissionMiddleware(1))], 
    response_model=permission_schema.PermissionResponse)
def create_permission(permission: permission_schema.PermissionCreate, service: PermissionService = Depends(get_permission_service)):
    return service.create(permission)

@router.put("/{id}", 
    dependencies=[Depends(auth_handler), Depends(PermissionMiddleware(3))], 
    response_model=permission_schema.PermissionResponse)
def update_permission(id: int, permission: permission_schema.PermissionUpdate, service: PermissionService = Depends(get_permission_service)):
    return service.update(id, permission)

@router.delete("/{id}", 
    dependencies=[Depends(auth_handler), Depends(PermissionMiddleware(6))]) 
def delete_permission(id: int, service: PermissionService = Depends(get_permission_service)):
    return service.delete(id)
