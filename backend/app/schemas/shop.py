from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic.alias_generators import to_camel


class ShopBaseModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True
    )


class ShopCreate(ShopBaseModel):
    name: str
    address: str
    contact_face: str
    phone_number: str
    email: EmailStr


class ShopView(ShopBaseModel):
    id: int
    name: str
    address: str
    contact_face: str
    phone_number: str
    email: EmailStr


class ShopUpdate(ShopBaseModel):
    id: int
    name: str
    address: str
    contact_face: str
    phone_number: str
    email: EmailStr


class ShopList(ShopBaseModel):
    count: int
    items: list[ShopView]
