from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_session
from app.db.repositories.product import ProductRepository
from app.db.repositories.shop import ShopRepository
from app.db.repositories.user import UserRepository
from app.services.product import ProductService
from app.services.shop import ShopService
from app.services.user import UserService


async def get_user_repository(
    session: AsyncSession = Depends(get_session)
) -> UserRepository:

    return UserRepository(session)


async def get_user_service(
    repository: UserRepository = Depends(get_user_repository)
) -> UserService:

    return UserService(repository)


async def get_product_repository(
    session: AsyncSession = Depends(get_session)
) -> ProductRepository:

    return ProductRepository(session)


async def get_product_service(
    repository: ProductRepository = Depends(get_product_repository)
) -> ProductService:

    return ProductService(repository)


async def get_shop_repository(
    session: AsyncSession = Depends(get_session)
) -> ShopRepository:

    return ShopRepository(session)


async def get_shop_service(
    repository: ShopRepository = Depends(get_shop_repository)
) -> ShopService:

    return ShopService(repository)
