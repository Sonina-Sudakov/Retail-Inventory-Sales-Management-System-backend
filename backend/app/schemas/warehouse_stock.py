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


class ProductInWarehouseList(WarehouseStockBaseModel):
    product: ProductView
    count: int
    total_quantity: int
    items: list[WarehouseStockViewWithoutProduct]


class WarehouseStockViewWithoutProduct(WarehouseStockBaseModel):
    cell_code: str
    quantity: int


class ChangeWarehouseStockCellCode(WarehouseStockBaseModel):
    id: int
    cell_code: str

class WarehouseSwapProductsView(WarehouseStockBaseModel):
    first_stock: WarehouseStockView
    second_stock: WarehouseStockView


class StoreProductInStock(WarehouseStockBaseModel):
    stock_id: int
    product_id: int
    quantity: int = 0
