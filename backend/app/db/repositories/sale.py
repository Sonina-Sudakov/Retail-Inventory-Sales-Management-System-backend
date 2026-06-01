from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.strategy_options import selectinload
from sqlalchemy.sql.expression import select

from app.db.models.sale import Sale
from app.db.repositories.base import BaseRepository


class SaleRepository(
    BaseRepository[Sale]
):
    def __init__(
        self,
        session: AsyncSession
    ):
        super().__init__(Sale, session)


    async def get_shop_sales(
        self,
        shop_id: int
    ) -> list[Sale]:
        
        stmt = (
            select(
                Sale
            )
            .where(Sale.shop_id == shop_id)
            .options(
                selectinload(Sale.shop),
                selectinload(Sale.user)
            )
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all())
