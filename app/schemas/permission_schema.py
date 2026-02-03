from pydantic import BaseModel
from typing import Optional

class PermissionBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None

class PermissionResponse(PermissionBase):
    id: int

    model_config = {
        "from_attributes": True
    }
