from sqlalchemy.orm import Session
from app.models.role import Role
from app.models.permission import Permission

def seed_roles(db: Session):
    roles = [
        {"id": 1, "name": "Super User"},
        {"id": 2, "name": "User"},
    ]

    existing_roles = db.query(Role).filter(Role.id.in_([1, 2])).count()
    if existing_roles == 0:
        for role in roles:
            db.add(Role(**role))
        db.commit()
        print("✅ Seeder roles successfully executed.")
    else:
        print("⚠️ Seeder roles already exist, not re-added.")

def seed_permissions(db: Session):
    permissions = [
        {"id": 1, "name": "Can create user"},
        {"id": 2, "name": "Can view users"},
        {"id": 3, "name": "Can update user"},
        {"id": 4, "name": "Can deactivate user"},
        {"id": 5, "name": "Can activate user"},
        {"id": 6, "name": "Can delete user"},
        {"id": 7, "name": "Can create role"},
        {"id": 8, "name": "Can view roles"},
        {"id": 9, "name": "Can update role"},
        {"id": 10, "name": "Can delete role"},
    ]

    existing_permissions = db.query(Permission).filter(Permission.id.in_([p["id"] for p in permissions])).count()
    if existing_permissions == 0:
        for permission in permissions:
            db.add(Permission(**permission))
        db.commit()
        print("✅ Seeder permissions successfully executed.")
    else:
        print("⚠️ Seeder permissions already exist, not re-added.")

def run_seeders(db: Session):
    print("🚀 Running seeders...")
    seed_roles(db)
    seed_permissions(db)
    print("✅ All seeders have finished running.")
