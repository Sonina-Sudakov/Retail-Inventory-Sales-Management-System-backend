from pydantic import BaseModel

from app.enums import UserRole


class UserCreateDTO(BaseModel):
    username: str
    fullname: str
    password: str
    role: UserRole


class UserViewDTO(BaseModel):
    id: int
    username: str
    fullname: str
    password: str
    role: UserRole


class UserListDTO(BaseModel):
    count: int
    items: list[UserViewDTO]


class UserUpdatePasswordDTO(BaseModel):
    id: int
    password: str


class UserUpdateFullnameDTO(BaseModel):
    id: int
    fullname: str
