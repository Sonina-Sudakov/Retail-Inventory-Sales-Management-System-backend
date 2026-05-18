from app.db.models.user import User
from app.db.repositories.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(
    BaseRepository[User]
):
    def __init__(
        self,
        session: AsyncSession
    ):
        super().__init__(User, session)

    
    async def update_password(
        self,
        user: User,
        new_hashed_password: str
    ) -> User:

        user.hash_password = new_hashed_password

        self.session.add(user)

        await self.session.flush()

        await self.session.refresh(user)

        return user


    async def update_fullname(
        self,
        user: User,
        new_fullname: str
    ) -> User:

        user.fullname = new_fullname

        self.session.add(user)

        await self.session.flush()

        await self.session.refresh(user)

        return user
