from datetime import datetime

from pydantic import BaseModel

from app.schemas.product import ProductView
from app.schemas.shop import ShopView
from app.schemas.user import UserView


class OrderCreate(BaseModel):
    shop_id: int 
    created_by_id: int
    count: int
    items: list[OrderItemCreate]


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int


class OrderDetailedView(BaseModel):
    id: int
    shop: ShopView
    created_by: UserView
    status: str
    created_at: datetime
    accepted_at: datetime | None = None
    count: int
    items: list[OrderItemView]


class OrderItemView(BaseModel):
    order_id: int
    product: ProductView
    quantity: int


class OrderView(BaseModel):
    id: int
    shop: OrderShopView
    created_by: OrderUserView
    status: str
    created_at: datetime
    accepted_at: datetime | None = None


class OrderList(BaseModel):
    count: int
    items: list[OrderView]


class OrderUpdateStatus(BaseModel):
    id: int
    status: str


class OrderShopView(BaseModel):
    id: int
    name: str


class OrderUserView(BaseModel):
    id: int
    fullname: str
