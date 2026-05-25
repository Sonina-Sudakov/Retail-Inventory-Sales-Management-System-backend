from app.enums import UserRole
from pydantic import BaseModel, ConfigDict


class UserBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserCreateDTO(UserBaseModel):
    username: str
    fullname: str
    password: str
    role: UserRole


class UserViewDTO(UserBaseModel):
    id: int
    username: str
    fullname: str
    role: str


class UserListDTO(UserBaseModel):
    count: int
    items: list[UserViewDTO]


class UserUpdatePasswordDTO(UserBaseModel):
    id: int
    password: str


class UserUpdateFullnameDTO(UserBaseModel):
    id: int
    fullname: str
