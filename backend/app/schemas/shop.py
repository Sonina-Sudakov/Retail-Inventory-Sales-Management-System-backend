from pydantic import BaseModel, EmailStr


class ShopCreate(BaseModel):
    name: str
    address: str
    contact_face: str
    phone_number: str
    email: EmailStr


class ShopView(BaseModel):
    id: int
    name: str
    address: str
    contact_face: str
    phone_number: str
    email: EmailStr


class ShopUpdate(BaseModel):
    id: int
    name: str
    address: str
    contact_face: str
    phone_number: str
    email: EmailStr


class ShopList(BaseModel):
    count: int
    items: list[ShopView]
