from sqlalchemy.orm import Session
from typing import List, Optional
from app.models import role_model
from app.schemas import role_schema

class RoleRepository:
    def __init__(self, db: Session):
        """
        Inisialisasi class dengan session database.
        """
        self.db = db

    def create_role(self, role: role_schema.RoleCreate) -> role_model.Role:
        db_role = role_model.Role(
            name=role.name,
            code=role.code,
            description=role.description
        )
        self.db.add(db_role)
        self.db.commit()
        self.db.refresh(db_role)
        return db_role

    def get_roles(self) -> List[role_model.Role]:
        return self.db.query(role_model.Role).all()

    def get_role_by_id(self, role_id: int) -> Optional[role_model.Role]:
        return self.db.query(role_model.Role).filter(role_model.Role.id == role_id).first()

    def get_role_by_code(self, code: str) -> Optional[role_model.Role]:
        return self.db.query(role_model.Role).filter(role_model.Role.code == code).first()
    
    def get_role_by_name(self, name: str) -> Optional[role_model.Role]:
        return self.db.query(role_model.Role).filter(role_model.Role.name == name).first()

    def update_role(self, role_id: int, role: role_schema.RoleUpdate) -> Optional[role_model.Role]:
        db_role = self.get_role_by_id(role_id)
        if not db_role:
            return None

        if role.name is not None:
            db_role.name = role.name
        if role.code is not None:
            db_role.code = role.code
        if role.description is not None:
            db_role.description = role.description
        
        self.db.commit()
        self.db.refresh(db_role)
        return db_role

    def delete_role(self, role_id: int) -> bool:
        db_role = self.get_role_by_id(role_id)
        if not db_role:
            return False

        self.db.delete(db_role)
        self.db.commit()
        return True
