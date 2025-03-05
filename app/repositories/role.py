from sqlalchemy.orm import Session

from app.models.role import Role
from app.schemas import RoleCreate


def create_role(db: Session, role: RoleCreate):
    existing_role = db.query(Role).filter(
        Role.name == role.name,
    ).first()

    if existing_role:
        return None

    db_role = Role(name=role.name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def get_roles(db: Session):
    return db.query(Role).all()