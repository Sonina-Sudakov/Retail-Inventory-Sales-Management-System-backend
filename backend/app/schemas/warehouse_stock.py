from pydantic import BaseModel

from app.schemas.product import ProductView


class WarehouseStockCreate(BaseModel):
    cell_code: str
    product_id: int
    quantity: int


class WarehouseStockView(BaseModel):
    id: int
    cell_code: str
    product_id: ProductView
    quantity: int


class WarehouseStockUpdate(BaseModel):
    id: int
    cell_code: str
    product_id: int
    quantity: int


class WarehouseStockList(BaseModel):    
    count: int
    items: list[WarehouseStockView]
