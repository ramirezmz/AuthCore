from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional


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


class UserListAllResponse(BaseModel):
    total: int
    users: list[UserResponse]


class AvailableUserUpdateRequest(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    role: Optional[RoleEnum] = None
