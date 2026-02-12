from sqlalchemy.orm import Session
from sqlalchemy import insert, delete, select, and_
from typing import List, Optional
from app.models.role_permission_model import role_permissions
from app.schemas import role_permission_schema

class RolePermissionRepository:
    def __init__(self, db: Session):
        self.db = db

    def assign_permission(self, role_id: int, permission_id: int):
        """
        Menambahkan (assign) satu permission ke sebuah role.
        """
        stmt = insert(role_permissions).values(role_id=role_id, permission_id=permission_id)
        self.db.execute(stmt)
        self.db.commit()

    def bulk_assign_permissions(self, role_id: int, permission_ids: List[int]):
        """
        Menambahkan banyak permission sekaligus ke sebuah role.
        """
        # Siapkan data untuk bulk insert
        values = [{"role_id": role_id, "permission_id": pid} for pid in permission_ids]
        if values:
            stmt = insert(role_permissions).values(values)
            self.db.execute(stmt)
            self.db.commit()

    def revoke_permission(self, role_id: int, permission_id: int):
        """
        Mencabut (menghapus) akses permission dari sebuah role.
        """
        stmt = delete(role_permissions).where(
            and_(role_permissions.c.role_id == role_id, role_permissions.c.permission_id == permission_id)
        )
        self.db.execute(stmt)
        self.db.commit()

    def get_role_permissions(self, role_id: int) -> List[int]:
        """
        Mendapatkan daftar permission_id yang dimiliki oleh role tertentu.
        """
        # Mengembalikan list permission_id
        stmt = select(role_permissions.c.permission_id).where(role_permissions.c.role_id == role_id)
        result = self.db.execute(stmt).scalars().all()
        return list(result)
    
    def check_permission_exists(self, role_id: int, permission_id: int) -> bool:
        """
        Mengecek apakah permission tertentu sudah diberikan ke role.
        """
        stmt = select(role_permissions).where(
            and_(role_permissions.c.role_id == role_id, role_permissions.c.permission_id == permission_id)
        )
        result = self.db.execute(stmt).first()
        return result is not None
