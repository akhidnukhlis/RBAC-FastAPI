from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PermissionBase(BaseModel):
    name: str

class PermissionCreate(PermissionBase):
    created_by: Optional[str] = None

class PermissionUpdate(BaseModel):
    name: Optional[str] = None
    updated_by: Optional[str] = None

class PermissionResponse(PermissionBase):
    id: int
    created_at: datetime
    created_by: Optional[str]
    updated_at: Optional[datetime]
    updated_by: Optional[str]
    deleted_at: Optional[datetime]
    deleted_by: Optional[str]

    model_config = {
        "from_attributes": True
    }
