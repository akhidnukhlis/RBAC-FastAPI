from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Permission(Base):
    __tablename__ = "permissions"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    code = Column(String, unique=True, index=True) # e.g., 'user:create', 'user:view'
    description = Column(String, nullable=True)
