from app.db.models.product import Product
from app.db.repositories.base_repository import BaseRepository
from sqlalchemy.ext.asyncio.session import AsyncSession


class ProductRepository(
    BaseRepository[Product]
):
    def __init__(
        self,
        session: AsyncSession
    ):
        super().__init__(Product, session)
