from pydantic import BaseModel
from typing import Optional

class RoleBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None

class RoleResponse(RoleBase):
    id: int

    model_config = {
        "from_attributes": True
    }
