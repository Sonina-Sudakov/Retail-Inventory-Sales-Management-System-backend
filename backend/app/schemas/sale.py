from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from app.schemas.product import ProductViewDTO
from app.schemas.shop import ShopViewDTO
from app.schemas.user import UserViewDTO


class SaleCreateDTO(BaseModel):
    shop_id: int
    user_id: int
    count: int
    items: list[SaleItemCreateDTO] 


class SaleItemCreateDTO(BaseModel):
    product_id: int
    quantity: int
    price: Decimal


class SaleDetailedViewDTO(BaseModel):
    id: int
    shop: ShopViewDTO
    user: UserViewDTO
    count: int
    items: list[SaleItemViewDTO]
    created_at: datetime


class SaleItemViewDTO(BaseModel):
    sale_id: int
    product: ProductViewDTO
    quantity: int
    price: Decimal


class SaleViewDTO(BaseModel):
    id: int
    shop: SaleShopViewDTO
    user: SaleUserViewDTO
    created_at: datetime


class SaleListDTO(BaseModel):
    count: int
    items: list[SaleViewDTO]


class SaleShopViewDTO(BaseModel):
    id: int
    name: str


class SaleUserViewDTO(BaseModel):
    id: int
    fullname: str
