from datetime import datetime

from pydantic import BaseModel

from app.schemas.product import ProductViewDTO
from app.schemas.shop import ShopViewDTO
from app.schemas.user import UserViewDTO


class OrderCreateDTO(BaseModel):
    shop_id: int 
    created_by_id: int
    count: int
    items: list[OrderItemCreateDTO]


class OrderItemCreateDTO(BaseModel):
    product_id: int
    quantity: int


class OrderDetailedViewDTO(BaseModel):
    id: int
    shop: ShopViewDTO
    created_by: UserViewDTO
    status: str
    created_at: datetime
    accepted_at: datetime | None = None
    count: int
    items: list[OrderItemViewDTO]


class OrderItemViewDTO(BaseModel):
    order_id: int
    product: ProductViewDTO
    quantity: int


class OrderViewDTO(BaseModel):
    id: int
    shop: OrderShopViewDTO
    created_by: OrderUserViewDTO
    status: str
    created_at: datetime
    accepted_at: datetime | None = None


class OrderListDTO(BaseModel):
    count: int
    items: list[OrderViewDTO]


class OrderUpdateStatusDTO(BaseModel):
    id: int
    status: str


class OrderShopViewDTO(BaseModel):
    id: int
    name: str


class OrderUserViewDTO(BaseModel):
    id: int
    fullname: str
