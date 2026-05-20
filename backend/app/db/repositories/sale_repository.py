from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.strategy_options import selectinload
from sqlalchemy.sql.expression import select

from app.db.models.sale import Sale
from app.db.models.sale_item import SaleItem
from app.db.repositories.base_repository import BaseRepository


class SaleRepository(
    BaseRepository[Sale]
):
    def __init__(
        self,
        session: AsyncSession
    ):
        super().__init__(Sale, session)


    async def get_full_sale_by_id(
        self,
        id: int
    ) -> Sale | None:
        sale = await self.get_by_id(
            id,
            options=[
                selectinload(Sale.shop),
                selectinload(Sale.user),
                selectinload(Sale.sale_items)
            ]
        )

        return sale


    async def get_shop_sales(
        self,
        shop_id: int
    ) -> list[Sale]:
        
        stmt = select(Sale).where(Sale.shop_id == shop_id)

        result = await self.session.execute(stmt)

        return list(result.scalars().all())


    async def save_sale_item(
        self,
        entity: SaleItem
    ) -> None:

        self.session.add(entity)

        await self.session.flush()
