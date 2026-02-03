from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Status(Base):
    __tablename__ = "statuses"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
