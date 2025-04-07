from pydantic import BaseModel

class TenantsBase(BaseModel):
    name: str

class TenantsCreate(BaseModel):
    name: str

class TenantsResponse(TenantsBase):
    id: int

    model_config = {
        "from_attributes": True
    }