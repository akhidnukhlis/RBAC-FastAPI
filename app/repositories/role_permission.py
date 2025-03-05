from sqlalchemy.orm import Session
from app.models import RolePermission
from app.schemas import RolePermissionCreate


def create_role_permission(db: Session, role_perm: RolePermissionCreate):
    existing_role_perm = db.query(RolePermission).filter(
        RolePermission.role_id == role_perm.role_id,
        RolePermission.permission_id == role_perm.permission_id
    ).first()

    if existing_role_perm:
        return None

    new_role_perm = RolePermission(
        role_id=role_perm.role_id,
        permission_id=role_perm.permission_id
    )

    db.add(new_role_perm)
    db.commit()
    db.refresh(new_role_perm)

    return new_role_perm

def delete_role_permission(db: Session, role_perm: RolePermissionCreate):
    db_role_perm = db.query(RolePermission).filter_by(
        role_id=role_perm.role_id, permission_id=role_perm.permission_id
    ).first()

    if not db_role_perm:
        return None

    db.delete(db_role_perm)
    db.commit()
    return db_role_perm

def get_all_role_permissions(db: Session):
    return db.query(RolePermission).all()

def check_role_permission(db: Session, role_id: int, permission_id: int) -> bool:
    return db.query(RolePermission).filter_by(role_id=role_id, permission_id=permission_id).first() is not None
