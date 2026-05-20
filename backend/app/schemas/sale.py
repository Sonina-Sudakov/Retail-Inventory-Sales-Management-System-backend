from datetime import datetime
from app.schemas.shop import ShopViewDTO
from app.schemas.user import UserViewDTO
from app.schemas.product import ProductViewDTO
from pydantic import BaseModel

class SaleCreateDTO(BaseModel):
    shop_id: int
    user_id: int
    count: int
    items: list[SaleItemCreateDTO] 


class SaleItemCreateDTO(BaseModel):
    product_id: int
    quantity: int
    price: float


class SaleDetailedViewDTO(BaseModel):
    id: int
    shop: ShopViewDTO
    user: UserViewDTO
    count: int
    items: list[SaleItemViewDTO]


class SaleItemViewDTO(BaseModel):
    sale_id: int
    product: ProductViewDTO
    quantity: int
    price: float


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
