from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import select

from app.db.models.product import Product
from app.db.models.warehouse_stock import WarehouseStock
from app.db.repositories.base_repository import BaseRepository


class WarehouseStockRepository(
    BaseRepository[WarehouseStock]
):
    def __init__(
        self,
        session: AsyncSession
    ):
        super().__init__(WarehouseStock, session)


    async def get_product_in_warehouse(
        self,
        product_id: int
    ) -> list[WarehouseStock]:
        
        stmt = (
            select(
                WarehouseStock,
                Product.name,
                Product.unit
            )
            .join(Product)
            .where(WarehouseStock.product_id == product_id))

        result = await self.session.execute(stmt)

        return list(result.scalars().all())


    async def get_warehouse_stocks(
        self
    ) -> list[WarehouseStock]:
        
        stmt = (
            select(
                WarehouseStock,
                Product.name,
                Product.unit
            )
            .join(Product)
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all())
