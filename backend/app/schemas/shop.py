from pydantic import BaseModel, EmailStr


class ShopCreateDTO(BaseModel):
    name: str
    address: str
    contact_face: str
    phone_number: str
    email: EmailStr


class ShopViewDTO(BaseModel):
    id: int
    name: str
    address: str
    contact_face: str
    phone_number: str
    email: EmailStr


class ShopUpdateDTO(BaseModel):
    id: int
    name: str
    address: str
    contact_face: str
    phone_number: str
    email: EmailStr


class ShopListDTO(BaseModel):
    count: int
    items: list[ShopViewDTO]
