from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.db.models.product import Product
from app.db.repositories.base import BaseRepository


class ProductRepository(
    BaseRepository[Product]
):
    def __init__(
        self,
        session: AsyncSession
    ):
        super().__init__(Product, session)


    async def get_by_name(
        self, 
        name: str
    ) -> Product | None:

        stmt = select(Product).where(Product.name == name)

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()
