from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.expression import select

from app.db.models.warehouse_stock import WarehouseStock
from app.db.repositories.base import BaseRepository


class WarehouseStockRepository(
    BaseRepository[WarehouseStock]
):
    def __init__(
        self,
        session: AsyncSession
    ):
        super().__init__(WarehouseStock, session)


    async def get_stock_by_cell_code(
        self,
        cell_code: str
    ) -> WarehouseStock | None:
        
        stmt = (
            select(
                WarehouseStock
            )
            .where(WarehouseStock.cell_code == cell_code)
            .options(selectinload(WarehouseStock.product))
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()


    async def get_product_in_warehouse(
        self,
        product_id: int
    ) -> list[WarehouseStock]:
        
        stmt = (
            select(
                WarehouseStock
            )
            .where(WarehouseStock.product_id == product_id)
            .options(selectinload(WarehouseStock.product))
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all())


    async def get_warehouse_stocks(
        self
    ) -> list[WarehouseStock]:
        
        stmt = (
            select(
                WarehouseStock,
            )
            .options(selectinload(WarehouseStock.product))
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all())
