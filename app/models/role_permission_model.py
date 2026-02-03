from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.core.database import Base

# Association Table (Many-to-Many)
role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('public.roles.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('public.permissions.id'), primary_key=True),
    schema='public'
)
