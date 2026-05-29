from app.enums import UserRole
from pydantic import BaseModel, ConfigDict


class UserBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBaseModel):
    username: str
    fullname: str
    password: str
    role: UserRole


class UserView(UserBaseModel):
    id: int
    username: str
    fullname: str
    role: str


class UserList(UserBaseModel):
    count: int
    items: list[UserView]


class UserUpdatePassword(UserBaseModel):
    id: int
    old_password: str
    new_password: str


class UserUpdateFullname(UserBaseModel):
    id: int
    new_fullname: str
