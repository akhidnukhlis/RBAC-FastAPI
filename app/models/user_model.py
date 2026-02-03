from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

import uuid
from app.models.role_model import Role
from app.models.status_model import Status

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "public"}

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role_id = Column(Integer, ForeignKey("public.roles.id"), nullable=True)  # ID role for RBAC
    status_id = Column(Integer, ForeignKey("public.statuses.id"), default=1)
    access_token = Column(String, unique=True, nullable=True)
    is_active = Column(Boolean, default=False)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    created_by = Column(String(255), nullable=True)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_by = Column(String(255), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_by = Column(String(255), nullable=True)

    role = relationship("Role")
    status = relationship("Status")