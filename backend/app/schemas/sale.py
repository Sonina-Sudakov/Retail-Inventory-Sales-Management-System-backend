from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from app.schemas.product import ProductView
from app.schemas.shop import ShopView
from app.schemas.user import UserView


class SaleBaseModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True
    )


class SaleCreate(SaleBaseModel):
    shop_id: int
    user_id: int
    count: int
    items: list[SaleItemCreate] 


class SaleItemCreate(SaleBaseModel):
    product_id: int
    quantity: int
    price: Decimal


class SaleDetailedView(SaleBaseModel):
    id: int
    shop: ShopView
    user: UserView
    count: int
    items: list[SaleItemView]
    created_at: datetime


class SaleItemView(SaleBaseModel):
    sale_id: int
    product: ProductView
    quantity: int
    price: Decimal


class SaleView(SaleBaseModel):
    id: int
    shop: SaleShopView
    user: SaleUserView
    created_at: datetime


class SaleList(SaleBaseModel):
    count: int
    items: list[SaleView]


class SaleShopView(SaleBaseModel):
    id: int
    name: str


class SaleUserView(SaleBaseModel):
    id: int
    fullname: str
