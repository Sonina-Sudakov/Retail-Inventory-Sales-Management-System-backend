from pydantic import BaseModel

from app.schemas.product import ProductView


class ShopStockCreate(BaseModel):
    shop_id: int
    product_id: int
    min_quantity: int
    quantity: int


class ShopStockView(BaseModel):
    product: ProductView
    min_quantity: int
    quantity: int


class ShopStockUpdate(BaseModel):
    shop_id: int
    product_id: int
    min_quantity: int
    quantity: int


class ShopStockList(BaseModel):
    shop: ShopStockShopView
    count: int
    items: list[ShopStockView]


class ShopStockShopView(BaseModel):
    id: int
    name: str
