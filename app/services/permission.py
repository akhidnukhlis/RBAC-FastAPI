from fastapi import HTTPException

from sqlalchemy.orm import Session
import app.repositories.permission as permission_repo
from app.schemas.permission import PermissionCreate, PermissionUpdate

def create_permission(db: Session, permission_data: PermissionCreate):
    new_permission = permission_repo.create_permission(db, permission_data)
    if not new_permission:
        raise HTTPException(status_code=409, detail="Permission already exists")

    return new_permission

def get_permissions(db: Session):
    return permission_repo.get_permissions(db)

def get_permission_by_id(db: Session, permission_id: int):
    permission = permission_repo.get_permission_by_id(db, permission_id)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    return permission

def update_permission(db: Session, permission_id: int, permission_data: PermissionUpdate):
    updated_permission = permission_repo.update_permission(db, permission_id, permission_data)
    if not updated_permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    return updated_permission

def soft_delete_permission(db: Session, permission_id: int, deleted_by: str):
    permission = permission_repo.soft_delete_permission(db, permission_id, deleted_by)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    return {"message": "Permission deleted successfully"}

def restore_permission(db: Session, permission_id: int):
    permission = permission_repo.restore_permission(db, permission_id)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found or not deleted")

    return {"message": "Permission restored successfully"}
