from pydantic import BaseModel, ConfigDict

from app.schemas.product import ProductView
from app.schemas.shop import ShopView


class ShopStockBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ShopStockCreate(ShopStockBaseModel):
    shop_id: int
    product_id: int
    min_quantity: int
    quantity: int


class ShopStockView(ShopStockBaseModel):
    shop: ShopView
    product: ProductView
    min_quantity: int
    quantity: int


class ShopStockWithProductView(ShopStockBaseModel):
    product: ProductView
    min_quantity: int
    quantity: int


class ShopStockWithShopView(ShopStockBaseModel):
    shop: ShopView
    min_quantity: int
    quantity: int


class ProductInShopsView(ShopStockBaseModel):
    product: ProductView
    count: int
    items: list[ShopStockWithShopView]


class ShopStockUpdate(ShopStockBaseModel):
    shop_id: int
    product_id: int
    min_quantity: int
    quantity: int


class ShopStockList(ShopStockBaseModel):
    shop: ShopView
    count: int
    items: list[ShopStockWithProductView]


class UpdateShopStockQuantity(ShopStockBaseModel):
    shop_id: int
    product_id: int 
    change: int


class UpdateShopStockMinQuantity(ShopStockBaseModel):
    shop_id: int
    product_id: int 
    min_quantity: int


class ShopStockShopView(ShopStockBaseModel):
    id: int
    name: str
