from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.schemas import RolePermissionCreate
from app.repositories import role_permissions

def add_role_permission(db: Session, role_perm: RolePermissionCreate):
    new_role_perm = role_permission.create_role_permission(db, role_perm)
    if not new_role_perm:
        raise HTTPException(status_code=400, detail="Role-Permission already exists")

    return new_role_perm

def remove_role_permission(db: Session, role_perm: RolePermissionCreate):
    return role_permission.delete_role_permission(db, role_perm)

def fetch_all_role_permissions(db: Session):
    return role_permission.get_all_role_permissions(db)
