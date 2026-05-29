from app.db.dependencies import get_session
from app.db.repositories.user import UserRepository
from app.services.user import UserService
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_repository(
    session: AsyncSession = Depends(get_session)
) -> UserRepository:

    return UserRepository(session)


async def get_user_service(
    repository: UserRepository = Depends(get_user_repository)
) -> UserService:

    return UserService(repository)
