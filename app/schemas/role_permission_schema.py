from pydantic import BaseModel
from typing import List

class RolePermissionBase(BaseModel):
    role_id: int
    permission_id: int

class RolePermissionCreate(RolePermissionBase):
    pass

class RolePermissionBatchCreate(BaseModel):
    role_id: int
    permission_ids: List[int]

class RolePermissionResponse(RolePermissionBase):
    model_config = {
        "from_attributes": True
    }
