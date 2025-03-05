from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.permission import create_permission, get_permissions, get_permission_by_id, update_permission, soft_delete_permission, restore_permission
from app.schemas.permission import PermissionCreate, PermissionUpdate, PermissionResponse
from app.core.database import get_db

router = APIRouter(prefix="/permissions", tags=["Permissions"])

@router.post("/", response_model=PermissionResponse)
def create_permission(permission: PermissionCreate, db: Session = Depends(get_db)):
    return create_permission(db, permission)

@router.get("/", response_model=list[PermissionResponse])
def get_permissions(db: Session = Depends(get_db)):
    return get_permissions(db)

@router.get("/{id}", response_model=PermissionResponse)
def get_permission(id: int, db: Session = Depends(get_db)):
    return get_permission_by_id(db, id)

@router.put("/{id}", response_model=PermissionResponse)
def update_permission(id: int, permission_data: PermissionUpdate, db: Session = Depends(get_db)):
    return update_permission(db, id, permission_data)

@router.delete("/{id}")
def soft_delete_permission(id: int, deleted_by: str, db: Session = Depends(get_db)):
    return soft_delete_permission(db, id, deleted_by)

@router.post("/{id}/restore")
def restore_permission(id: int, db: Session = Depends(get_db)):
    return restore_permission(db, id)
