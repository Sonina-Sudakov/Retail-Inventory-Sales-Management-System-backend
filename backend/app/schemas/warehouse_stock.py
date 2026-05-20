from pydantic import BaseModel

from app.schemas.product import ProductViewDTO


class WarehouseStockCreateDTO(BaseModel):
    cell_code: str
    product_id: int
    quantity: int


class WarehouseStockViewDTO(BaseModel):
    id: int
    cell_code: str
    product_id: ProductViewDTO
    quantity: int


class WarehouseStockUpdate(BaseModel):
    id: int
    cell_code: str
    product_id: int
    quantity: int


class WarehouseStockListDTO(BaseModel):    
    count: int
    items: list[WarehouseStockViewDTO]
