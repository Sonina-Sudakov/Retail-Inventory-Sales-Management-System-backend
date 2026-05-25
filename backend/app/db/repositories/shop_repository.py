from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select

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


    async def get_by_phone_number(
        self,
        phone_number: str
    ) -> Shop | None:

        stmt = select(Shop).where(Shop.phone_number == phone_number)

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()
