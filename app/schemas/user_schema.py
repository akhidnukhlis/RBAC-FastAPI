from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role_id: Optional[int] = None
    is_active: Optional[bool] = True

class UserUpdate(UserBase):
    password: Optional[str] = None
    role_id: Optional[int] = None
    status_id: Optional[int] = None
    is_active: Optional[bool] = None

class UserRegister(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class RoleInfo(BaseModel):
    id: int
    name: str = Field(validation_alias="name")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }

class StatusInfo(BaseModel):
    id: int
    name: str = Field(validation_alias="name")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }

class UserResponse(UserBase):
    id: str
    role: Optional[RoleInfo] = None
    status: Optional[StatusInfo] = None

    model_config = {
        "from_attributes": True
    }