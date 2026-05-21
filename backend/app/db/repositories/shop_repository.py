from sqlalchemy.ext.asyncio.session import AsyncSession

from app.db.models.shop import Shop
from app.db.repositories.base_repository import BaseRepository


class ShopRepository(
    BaseRepository[Shop]
):
    def __init__(
        self,
        session: AsyncSession
    ):
        super().__init__(Shop, session)
