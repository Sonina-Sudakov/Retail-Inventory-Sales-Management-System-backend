from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.product import ProductView
from app.schemas.shop import ShopView
from app.schemas.user import UserView


class ShipmentBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ShipmentCreate(ShipmentBaseModel):
    from_location: str
    to_shop_id: int | None = None
    created_by_id: int
    items: list[ShipmentItemCreate]


class ShipmentItemCreate(ShipmentBaseModel):
    product_id: int
    quantity: int


class ShipmentDetailedView(ShipmentBaseModel):
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


class ShipmentItemView(ShipmentBaseModel):
    shipment_id: int
    product: ProductView
    quantity: int


class ShipmentView(ShipmentBaseModel):
    id: int
    from_location: str
    to_shop: ShipmentShopView | None = None
    status: str
    created_by: ShipmentUserView | None = None
    created_at: datetime
    updated_at: datetime | None = None


class ShipmentList(ShipmentBaseModel):
    count: int
    items: list[ShipmentView]


class ShipmentShopView(ShipmentBaseModel):
    id: int
    name: str


class ShipmentUserView(ShipmentBaseModel):
    id: int
    fullname: str
