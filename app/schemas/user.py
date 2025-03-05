from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role_id: Optional[int] = None

class UserUpdate(UserBase):
    password: Optional[str] = None
    role_id: Optional[int] = None

class UserRegister(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    role_id: Optional[int] = None
    access_token: Optional[str] = None

    model_config = {
        "from_attributes": True
    }