from sqlalchemy.ext.asyncio.session import AsyncSession

from app.db.models.product import Product
from app.db.repositories.base_repository import BaseRepository


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

        return await self.session.get(
            self.model,
            name
        ) 
