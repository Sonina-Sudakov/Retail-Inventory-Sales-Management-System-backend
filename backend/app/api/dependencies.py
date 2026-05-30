from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_session
from app.db.models.shop import Shop
from app.db.repositories.product import ProductRepository
from app.db.repositories.shop import ShopRepository
from app.db.repositories.user import UserRepository
from app.db.repositories.order import OrderRepository
from app.services.product import ProductService
from app.services.shop import ShopService
from app.services.user import UserService
from app.services.order import OrderService


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


async def get_order_repository(
    session: AsyncSession = Depends(get_session)
) -> OrderRepository:

    return OrderRepository(session)


async def get_order_service(
    repository: OrderRepository = Depends(get_order_repository),
    shop_repository: ShopRepository = Depends(get_shop_repository),
    product_repository: ProductRepository = Depends(get_product_repository),
    user_repository: UserRepository = Depends(get_user_repository)
) -> OrderService:

    return OrderService(repository, shop_repository, product_repository, user_repository)
