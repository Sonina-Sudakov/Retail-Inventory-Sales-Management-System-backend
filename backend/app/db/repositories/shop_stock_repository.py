from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.expression import select

from app.db.models.product import Product
from app.db.models.shop import Shop
from app.db.models.shop_stock import ShopStock
from app.db.repositories.base_repository import BaseRepository


class ShopStockRepository(
    BaseRepository[ShopStock]
):
    def __init__(
        self,
        session: AsyncSession
    ):
        super().__init__(ShopStock, session)


    async def get_full_product_in_shop(
        self,
        shop_id: int,
        product_id: int
    ) -> ShopStock | None:
    
        stmt = (
            select(ShopStock)
            .options(selectinload(ShopStock.shop), selectinload(ShopStock.product))
            .where(ShopStock.shop_id == shop_id and ShopStock.product_id == product_id)
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()


    async def get_product_in_shop(
        self,
        shop_id: int,
        product_id: int
    ) -> ShopStock | None:
    
        stmt = (
            select(ShopStock)
            .where(ShopStock.shop_id == shop_id and ShopStock.product_id == product_id)
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()


    async def get_product_in_shops(
        self,
        product_id: int
    ) -> list[ShopStock]:
        
        stmt = (
            select(
                ShopStock,
                Shop.name,
                Shop.address
            )
            .join(Shop)
            .where(ShopStock.product == product_id))

        result = await self.session.execute(stmt)

        return list(result.scalars().all())


    async def get_shop_stocks(
        self,
        shop_id: int
    ) -> list[ShopStock]:
        
        stmt = (
            select(
                ShopStock,
                Product.name,
                Product.unit
            )
            .join(Product)
            .where(ShopStock.shop_id == shop_id)
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all())
