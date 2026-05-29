from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.db.repositories.base_repository import BaseRepository


class UserRepository(
    BaseRepository[User]
):
    def __init__(
        self,
        session: AsyncSession
    ):
        super().__init__(User, session)


    async def get_by_username(
        self,
        username: str
    ) -> User | None:

        return await self.session.get(
            self.model,
            username
        )
