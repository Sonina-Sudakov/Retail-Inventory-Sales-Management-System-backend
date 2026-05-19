from app.db.models.sale import Sale
from app.db.repositories.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select


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
        
        stmt = select(Sale).where(Sale.id == shop_id)

        result = await self.session.execute(stmt)

        return list(result.scalars().all())
