from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List, Optional, Dict

from app.repositories.permission_repository import PermissionRepository
from app.schemas import permission_schema

class PermissionService:
    def __init__(self, db: Session):
        """
        Inisialisasi Service dengan session database.
        """
        self.db = db
        self.repository = PermissionRepository(db)

    def create(self, permission_data: permission_schema.PermissionCreate):
        """Membuat permission baru dengan validasi kode dan nama."""
        # Cek kode unik
        if self.repository.get_permission_by_code(permission_data.code):
            raise HTTPException(status_code=400, detail="Permission code already exists")
        
        # Cek nama unik
        if self.repository.get_permission_by_name(permission_data.name):
            raise HTTPException(status_code=400, detail="Permission name already exists")

        return self.repository.create_permission(permission_data)

    def list_all(self):
        """Mendapatkan semua daftar permission."""
        return self.repository.get_permissions()

    def get_by_id(self, permission_id: int):
        """Mendapatkan permission berdasarkan ID."""
        permission = self.repository.get_permission_by_id(permission_id)
        if not permission:
            raise HTTPException(status_code=404, detail="Permission not found")
        return permission

    def update(self, permission_id: int, permission_data: permission_schema.PermissionUpdate):
        """Mengubah data permission dan validasi keberadaannya."""
        # Jika update kode, cek unik (kecuali milik sendiri)
        if permission_data.code:
             existing_permission = self.repository.get_permission_by_code(permission_data.code)
             if existing_permission and existing_permission.id != permission_id:
                 raise HTTPException(status_code=400, detail="Permission code already exists")

        updated_permission = self.repository.update_permission(permission_id, permission_data)
        if not updated_permission:
            raise HTTPException(status_code=404, detail="Permission not found")

        return updated_permission

    def delete(self, permission_id: int) -> Dict[str, str]:
        """Menghapus permission dan validasi keberadaannya."""
        success = self.repository.delete_permission(permission_id)
        if not success:
            raise HTTPException(status_code=404, detail="Permission not found")

        return {"message": "Permission deleted successfully"}
