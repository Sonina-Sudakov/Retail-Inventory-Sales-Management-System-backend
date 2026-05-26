from datetime import datetime

from pydantic import BaseModel

from app.schemas.product import ProductViewDTO
from app.schemas.shop import ShopViewDTO
from app.schemas.user import UserViewDTO


class ShipmentCreateDTO(BaseModel):
    from_location: str
    to_shop_id: int | None = None
    created_by_id: int
    items: list[ShipmentItemCreateDTO]


class ShipmentItemCreateDTO(BaseModel):
    product_id: int
    quantity: int


class ShipmentDetailedViewDTO(BaseModel):
    id: int
    from_location: str
    to_shop: ShopViewDTO | None = None
    status: str
    created_by: UserViewDTO
    accepted_by: UserViewDTO | None = None
    created_at: datetime
    updated_at: datetime | None = None
    count: int
    items: list[ShipmentItemViewDTO]


class ShipmentItemViewDTO(BaseModel):
    shipment_id: int
    product: ProductViewDTO
    quantity: int


class ShipmentViewDTO(BaseModel):
    id: int
    from_location: str
    to_shop: ShipmentShopViewDTO | None = None
    status: str
    created_by: ShipmentUserViewDTO | None = None
    created_at: datetime
    updated_at: datetime | None = None


class ShipmentListDTO(BaseModel):
    count: int
    items: list[ShipmentViewDTO]


class ShipmentShopViewDTO(BaseModel):
    id: int
    name: str


class ShipmentUserViewDTO(BaseModel):
    id: int
    fullname: str
