from sqlalchemy.orm import Session
from sqlalchemy import insert, delete, select, and_
from typing import List, Optional
from app.models.role_permission_model import role_permissions
from app.schemas import role_permission_schema

class RolePermissionRepository:
    def __init__(self, db: Session):
        self.db = db

    def assign_permission(self, role_id: int, permission_id: int):
        stmt = insert(role_permissions).values(role_id=role_id, permission_id=permission_id)
        self.db.execute(stmt)
        self.db.commit()

    def bulk_assign_permissions(self, role_id: int, permission_ids: List[int]):
        # Siapkan data untuk bulk insert
        values = [{"role_id": role_id, "permission_id": pid} for pid in permission_ids]
        if values:
            stmt = insert(role_permissions).values(values)
            self.db.execute(stmt)
            self.db.commit()

    def revoke_permission(self, role_id: int, permission_id: int):
        stmt = delete(role_permissions).where(
            and_(role_permissions.c.role_id == role_id, role_permissions.c.permission_id == permission_id)
        )
        self.db.execute(stmt)
        self.db.commit()

    def get_role_permissions(self, role_id: int) -> List[int]:
        # Mengembalikan list permission_id
        stmt = select(role_permissions.c.permission_id).where(role_permissions.c.role_id == role_id)
        result = self.db.execute(stmt).scalars().all()
        return list(result)
    
    def check_permission_exists(self, role_id: int, permission_id: int) -> bool:
        stmt = select(role_permissions).where(
            and_(role_permissions.c.role_id == role_id, role_permissions.c.permission_id == permission_id)
        )
        result = self.db.execute(stmt).first()
        return result is not None
