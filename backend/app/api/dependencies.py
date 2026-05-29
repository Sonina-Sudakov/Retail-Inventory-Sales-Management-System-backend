from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.user_repository import UserRepository
from app.db.session import get_session
from app.services.user import UserService


async def get_user_service(
    session: AsyncSession = Depends(get_session)
) -> UserService:

    user_repository = UserRepository(session)

    return UserService(
        session=session,
        user_repository=user_repository
    )
