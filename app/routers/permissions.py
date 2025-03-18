from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.permissions import create_permission, get_permissions, get_permission_by_id, update_permission, soft_delete_permission, restore_permission
from app.schemas.permissions import PermissionCreate, PermissionUpdate, PermissionResponse
from app.core.database import get_db
from app.middleware.permission_middleware import PermissionMiddleware
from app.middleware.auth_middleware import AuthMiddleware

router = APIRouter(prefix="/permissions", tags=["Permissions"])

@router.post("/", dependencies=[Depends(AuthMiddleware), Depends(PermissionMiddleware(3))], response_model=PermissionResponse)
def create_permission(permission: PermissionCreate, db: Session = Depends(get_db)):
    return create_permission(db, permission)

@router.get("/", dependencies=[Depends(AuthMiddleware), Depends(PermissionMiddleware(2))], response_model=list[PermissionResponse])
def get_permissions(db: Session = Depends(get_db)):
    return get_permissions(db)

@router.get("/{id}", dependencies=[Depends(AuthMiddleware), Depends(PermissionMiddleware(2))], response_model=PermissionResponse)
def get_permission(id: int, db: Session = Depends(get_db)):
    return get_permission_by_id(db, id)

@router.put("/{id}", dependencies=[Depends(AuthMiddleware), Depends(PermissionMiddleware(3))],response_model=PermissionResponse)
def update_permission(id: int, permission_data: PermissionUpdate, db: Session = Depends(get_db)):
    return update_permission(db, id, permission_data)

@router.delete("/{id}", dependencies=[Depends(AuthMiddleware), Depends(PermissionMiddleware(6))])
def soft_delete_permission(id: int, deleted_by: str, db: Session = Depends(get_db)):
    return soft_delete_permission(db, id, deleted_by)

@router.post("/{id}/restore", dependencies=[Depends(AuthMiddleware), Depends(PermissionMiddleware(7))],)
def restore_permission(id: int, db: Session = Depends(get_db)):
    return restore_permission(db, id)
