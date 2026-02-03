from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas import role_permission_schema, permission_schema
from app.core.database import db_manager as DBManager
from app.services.role_permission_service import RolePermissionService
from app.middleware.permission_middleware import PermissionMiddleware
from app.middleware.auth_middleware import auth_handler

router = APIRouter(prefix="/role-permissions", tags=["Role Permissions"])

def get_service(db: Session = Depends(DBManager.get_db)):
    return RolePermissionService(db)

@router.post("/assign", 
    dependencies=[Depends(auth_handler), Depends(PermissionMiddleware(18))], # code: role_permission:create
    summary="Assign permissions to a role (Bulk)"
)
def assign_permissions(
    data: role_permission_schema.RolePermissionBatchCreate, 
    service: RolePermissionService = Depends(get_service)
):
    return service.assign_permissions(data)

@router.get("/{role_id}", 
    dependencies=[Depends(auth_handler), Depends(PermissionMiddleware(19))], # code: role_permission:read
    response_model=List[permission_schema.PermissionResponse],
    summary="Get all permissions assigned to a role"
)
def get_role_permissions(
    role_id: int, 
    service: RolePermissionService = Depends(get_service)
):
    return service.get_role_permissions(role_id)

@router.delete("/{role_id}/{permission_id}", 
    dependencies=[Depends(auth_handler), Depends(PermissionMiddleware(20))], # code: role_permission:delete
    summary="Revoke a specific permission from a role"
)
def revoke_permission(
    role_id: int, 
    permission_id: int, 
    service: RolePermissionService = Depends(get_service)
):
    return service.revoke_permission(role_id, permission_id)
