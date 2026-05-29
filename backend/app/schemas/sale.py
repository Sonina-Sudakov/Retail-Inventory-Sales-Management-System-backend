from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from app.schemas.product import ProductView
from app.schemas.shop import ShopView
from app.schemas.user import UserView


class SaleCreate(BaseModel):
    shop_id: int
    user_id: int
    count: int
    items: list[SaleItemCreate] 


class SaleItemCreate(BaseModel):
    product_id: int
    quantity: int
    price: Decimal


class SaleDetailedView(BaseModel):
    id: int
    shop: ShopView
    user: UserView
    count: int
    items: list[SaleItemView]
    created_at: datetime


class SaleItemView(BaseModel):
    sale_id: int
    product: ProductView
    quantity: int
    price: Decimal


class SaleView(BaseModel):
    id: int
    shop: SaleShopView
    user: SaleUserView
    created_at: datetime


class SaleList(BaseModel):
    count: int
    items: list[SaleView]


class SaleShopView(BaseModel):
    id: int
    name: str


class SaleUserView(BaseModel):
    id: int
    fullname: str
