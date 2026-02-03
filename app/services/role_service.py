from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List, Optional, Dict

from app.repositories.role_repository import RoleRepository
from app.schemas import role_schema

class RoleService:
    def __init__(self, db: Session):
        """
        Inisialisasi Service dengan session database.
        """
        self.db = db
        self.repository = RoleRepository(db)

    def create(self, role_data: role_schema.RoleCreate):
        """Membuat role baru dengan validasi kode dan nama."""
        # Cek kode unik
        if self.repository.get_role_by_code(role_data.code):
            raise HTTPException(status_code=400, detail="Role code already exists")
        
        # Cek nama unik
        if self.repository.get_role_by_name(role_data.name):
            raise HTTPException(status_code=400, detail="Role name already exists")

        return self.repository.create_role(role_data)

    def list_all(self):
        """Mendapatkan semua daftar role."""
        return self.repository.get_roles()

    def get_by_id(self, role_id: int):
        """Mendapatkan role berdasarkan ID."""
        role = self.repository.get_role_by_id(role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        return role

    def update(self, role_id: int, role_data: role_schema.RoleUpdate):
        """Mengubah data role dan validasi keberadaannya."""
        # Jika update kode, cek unik (kecuali milik sendiri) - sederhana saja: cek if exists
        if role_data.code:
             existing_role = self.repository.get_role_by_code(role_data.code)
             if existing_role and existing_role.id != role_id:
                 raise HTTPException(status_code=400, detail="Role code already exists")

        updated_role = self.repository.update_role(role_id, role_data)
        if not updated_role:
            raise HTTPException(status_code=404, detail="Role not found")

        return updated_role

    def delete(self, role_id: int) -> Dict[str, str]:
        """Menghapus role dan validasi keberadaannya."""
        success = self.repository.delete_role(role_id)
        if not success:
            raise HTTPException(status_code=404, detail="Role not found")

        return {"message": "Role deleted successfully"}
