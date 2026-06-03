from datetime import datetime

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from app.schemas.product import ProductView
from app.schemas.shop import ShopView
from app.schemas.user import UserView


class OrderBaseModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True
    )


class OrderCreate(OrderBaseModel):
    to_shop_id: int 
    created_by_id: int
    count: int
    items: list[OrderItemCreate]


class OrderItemCreate(OrderBaseModel):
    product_id: int
    quantity: int


class OrderDetailedView(OrderBaseModel):
    id: int
    to_shop: ShopView
    created_by: UserView
    status: str
    created_at: datetime
    accepted_at: datetime | None = None
    items: list[OrderItemView]


class OrderItemView(OrderBaseModel):
    order_id: int
    product: ProductView
    quantity: int


class OrderView(OrderBaseModel):
    id: int
    to_shop: OrderShopView
    created_by: OrderUserView
    status: str
    created_at: datetime
    accepted_at: datetime | None = None


class OrderList(OrderBaseModel):
    count: int
    items: list[OrderView]


class OrderShopView(OrderBaseModel):
    id: int
    name: str


class OrderUserView(OrderBaseModel):
    id: int
    fullname: str
