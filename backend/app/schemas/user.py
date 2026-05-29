from pydantic import BaseModel, ConfigDict

from app.enums import UserRole


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
    password: str


class UserUpdateFullname(UserBaseModel):
    id: int
    fullname: str
