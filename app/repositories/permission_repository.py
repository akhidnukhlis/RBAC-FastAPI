from sqlalchemy.orm import Session
from typing import List, Optional
from app.models import permission_model
from app.schemas import permission_schema

class PermissionRepository:
    def __init__(self, db: Session):
        """
        Inisialisasi class dengan session database.
        """
        self.db = db

    def create_permission(self, permission: permission_schema.PermissionCreate) -> permission_model.Permission:
        db_permission = permission_model.Permission(
            name=permission.name,
            code=permission.code,
            description=permission.description
        )
        self.db.add(db_permission)
        self.db.commit()
        self.db.refresh(db_permission)
        return db_permission

    def get_permissions(self) -> List[permission_model.Permission]:
        return self.db.query(permission_model.Permission).all()

    def get_permission_by_id(self, permission_id: int) -> Optional[permission_model.Permission]:
        return self.db.query(permission_model.Permission).filter(permission_model.Permission.id == permission_id).first()

    def get_permission_by_code(self, code: str) -> Optional[permission_model.Permission]:
        return self.db.query(permission_model.Permission).filter(permission_model.Permission.code == code).first()
    
    def get_permission_by_name(self, name: str) -> Optional[permission_model.Permission]:
        return self.db.query(permission_model.Permission).filter(permission_model.Permission.name == name).first()

    def update_permission(self, permission_id: int, permission: permission_schema.PermissionUpdate) -> Optional[permission_model.Permission]:
        db_permission = self.get_permission_by_id(permission_id)
        if not db_permission:
            return None

        if permission.name is not None:
            db_permission.name = permission.name
        if permission.code is not None:
            db_permission.code = permission.code
        if permission.description is not None:
            db_permission.description = permission.description
        
        self.db.commit()
        self.db.refresh(db_permission)
        return db_permission

    def delete_permission(self, permission_id: int) -> bool:
        db_permission = self.get_permission_by_id(permission_id)
        if not db_permission:
            return False

        self.db.delete(db_permission)
        self.db.commit()
        return True
