from sqlalchemy.orm import Session
from app.models.permission import Permission
from app.schemas.permission import PermissionCreate, PermissionUpdate
from datetime import datetime
from fastapi import HTTPException

def create_permission(db: Session, permission_data: PermissionCreate):
    db_perm = db.query(Permission).filter(Permission.name == permission_data.name).first()
    if db_perm:
        return None

    new_permission = Permission(
        name=permission_data.name
    )
    db.add(new_permission)
    db.commit()
    db.refresh(new_permission)
    return new_permission

def get_permissions(db: Session):
    return db.query(Permission).all()

def get_permission_by_id(db: Session, permission_id: int):
    permission = db.query(Permission).filter(
        Permission.id == permission_id
    ).first()
    if not permission:
        return None

    return permission

def update_permission(db: Session, permission_id: int, permission_data: PermissionUpdate):
    permission = db.query(Permission).filter(
        Permission.id == permission_id
    ).first()
    if not permission:
        return None

    if permission_data.name:
        permission.name = permission_data.name
    if permission_data.updated_by:
        permission.updated_by = permission_data.updated_by
        permission.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(permission)
    return permission

def soft_delete_permission(db: Session, permission_id: int, deleted_by: str):
    permission = db.query(Permission).filter(
        Permission.id == permission_id
    ).first()
    if not permission:
        return False

    permission.deleted_at = datetime.utcnow()
    permission.deleted_by = deleted_by
    db.commit()

    return True

def restore_permission(db: Session, permission_id: int):
    permission = db.query(Permission).filter(
        Permission.id == permission_id
    ).first()
    if not permission:
        return False

    permission.deleted_at = None
    permission.deleted_by = None
    db.commit()

    return True
