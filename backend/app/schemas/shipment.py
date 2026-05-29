from datetime import datetime

from pydantic import BaseModel

from app.schemas.product import ProductView
from app.schemas.shop import ShopView
from app.schemas.user import UserView


class ShipmentCreate(BaseModel):
    from_location: str
    to_shop_id: int | None = None
    created_by_id: int
    items: list[ShipmentItemCreate]


class ShipmentItemCreate(BaseModel):
    product_id: int
    quantity: int


class ShipmentDetailedView(BaseModel):
    id: int
    from_location: str
    to_shop: ShopView | None = None
    status: str
    created_by: UserView
    accepted_by: UserView | None = None
    created_at: datetime
    updated_at: datetime | None = None
    count: int
    items: list[ShipmentItemView]


class ShipmentItemView(BaseModel):
    shipment_id: int
    product: ProductView
    quantity: int


class ShipmentView(BaseModel):
    id: int
    from_location: str
    to_shop: ShipmentShopView | None = None
    status: str
    created_by: ShipmentUserView | None = None
    created_at: datetime
    updated_at: datetime | None = None


class ShipmentList(BaseModel):
    count: int
    items: list[ShipmentView]


class ShipmentShopView(BaseModel):
    id: int
    name: str


class ShipmentUserView(BaseModel):
    id: int
    fullname: str
