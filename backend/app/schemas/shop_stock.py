from pydantic import BaseModel, ConfigDict

from app.schemas.product import ProductView


class ShopStockBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class ShopStockCreate(ShopStockBaseModel):
    shop_id: int
    product_id: int
    min_quantity: int
    quantity: int


class ShopStockView(ShopStockBaseModel):
    product: ProductView
    min_quantity: int
    quantity: int


class ShopStockUpdate(ShopStockBaseModel):
    shop_id: int
    product_id: int
    min_quantity: int
    quantity: int


class ShopStockList(ShopStockBaseModel):
    shop: ShopStockShopView
    count: int
    items: list[ShopStockView]


class ShopStockShopView(ShopStockBaseModel):
    id: int
    name: str
