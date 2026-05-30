from pydantic import BaseModel, ConfigDict

from app.schemas.product import ProductView


class WarehouseStockBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class WarehouseStockCreate(WarehouseStockBaseModel):
    cell_code: str
    product_id: int
    quantity: int


class WarehouseStockView(WarehouseStockBaseModel):
    id: int
    cell_code: str
    product_id: ProductView
    quantity: int


class WarehouseStockUpdate(WarehouseStockBaseModel):
    id: int
    cell_code: str
    product_id: int
    quantity: int


class WarehouseStockList(WarehouseStockBaseModel):
    count: int
    items: list[WarehouseStockView]
