from pydantic import BaseModel, EmailStr
from enum import Enum


class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"
    invited = "invited"


class UserCreateRequest(BaseModel):
    email: EmailStr
    name: str
    password: str
    role: RoleEnum = RoleEnum.user


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    name: str
    role: RoleEnum
    created_at: str
    updated_at: str
