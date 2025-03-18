from pydantic import BaseModel

class RoleBase(BaseModel):
    name: str

class RoleCreate(BaseModel):
    name: str

class RoleResponse(RoleBase):
    id: int

    model_config = {
        "from_attributes": True
    }