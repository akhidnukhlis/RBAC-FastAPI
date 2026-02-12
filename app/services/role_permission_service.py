from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List, Dict

from app.repositories import role_permission_repository, role_repository, permission_repository
from app.schemas import role_permission_schema

class RolePermissionService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = role_permission_repository.RolePermissionRepository(db)
        self.role_repo = role_repository.RoleRepository(db)
        self.perm_repo = permission_repository.PermissionRepository(db)

    def assign_permissions(self, data: role_permission_schema.RolePermissionBatchCreate):
        """
        Memberikan beberapa permission sekaligus ke sebuah role.
        Melewati (skip) permission yang duplikat atau tidak valid.
        """
        # 1. Validasi Role exist
        if not self.role_repo.get_role_by_id(data.role_id):
            raise HTTPException(status_code=404, detail="Role not found")
        
        # 2. Filter permission ID yang valid
        valid_perms = []
        for pid in data.permission_ids:
            if self.perm_repo.get_permission_by_id(pid):
                # 3. Cek apakah sudah di-assign (hindari unique violation/duplicate logic)
                if not self.repo.check_permission_exists(data.role_id, pid):
                    valid_perms.append(pid)
        
        # 4. Bulk Insert yang belum ada
        if valid_perms:
            self.repo.bulk_assign_permissions(data.role_id, valid_perms)
        
        return {"message": f"Successfully assigned {len(valid_perms)} permissions to Role ID {data.role_id}"}

    def revoke_permission(self, role_id: int, permission_id: int):
        """
        Mencabut permission tertentu dari sebuah role.
        """
        if not self.repo.check_permission_exists(role_id, permission_id):
             raise HTTPException(status_code=404, detail="Permission not assigned to this role")
        
        self.repo.revoke_permission(role_id, permission_id)
        return {"message": "Permission revoked successfully"}

    def get_role_permissions(self, role_id: int):
        """
        Mendapatkan semua permission yang dimiliki oleh role.
        """
        if not self.role_repo.get_role_by_id(role_id):
            raise HTTPException(status_code=404, detail="Role not found")
            
        perm_ids = self.repo.get_role_permissions(role_id)
        
        # Hydrate permission details (optional, but good for UI)
        perms = []
        for pid in perm_ids:
            p = self.perm_repo.get_permission_by_id(pid)
            if p:
                perms.append(p)
                
        return perms
