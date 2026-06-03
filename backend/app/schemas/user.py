from pydantic import BaseModel, ConfigDict, model_validator
from pydantic.alias_generators import to_camel

from app.enums import UserRole
from app.schemas.shop import ShopView


class UserBaseModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True
    )


class UserCreate(UserBaseModel):
    username: str
    fullname: str
    password: str
    works_in_shop_id: int | None = None
    role: UserRole

    @model_validator(mode="before")
    @classmethod
    def check_role_and_shop_dependency(cls, data: dict) -> dict:
        role = data.get("role")
        works_in_shop_id = data.get("works_in_shop_id")

        if role == UserRole.SHOPKEEPER and works_in_shop_id is None:
            raise ValueError("ShopKeeper must have works_in_shop_id populated.")

        if role == UserRole.STOREKEEPER and works_in_shop_id is not None:
            raise ValueError("StoreKeeper cannot have a works_in_shop_id.")

        return data


class UserView(UserBaseModel):
    id: int
    username: str
    fullname: str
    works_in_shop: ShopView | None = None
    role: str


class UserList(UserBaseModel):
    count: int
    items: list[UserView]


class UserUpdatePassword(UserBaseModel):
    id: int
    new_password: str


class UserUpdateFullname(UserBaseModel):
    id: int
    new_fullname: str


class UserUpdateWorkplace(UserBaseModel):
    id: int
    shop_id: int
