from pydantic import BaseModel

from app.schemas.product import ProductViewDTO


class ShopStockCreateDTO(BaseModel):
    shop_id: int
    product_id: int
    min_quantity: int
    quantity: int


class ShopStockViewDTO(BaseModel):
    product: ProductViewDTO
    min_quantity: int
    quantity: int


class ShopStockUpdate(BaseModel):
    shop_id: int
    product_id: int
    min_quantity: int
    quantity: int


class ShopStockListDTO(BaseModel):
    shop: ShopStockShopViewDTO
    count: int
    items: list[ShopStockViewDTO]


class ShopStockShopViewDTO(BaseModel):
    id: int
    name: str
