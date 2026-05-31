from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_session
from app.db.repositories import (OrderRepository, ProductRepository,
                                 SaleRepository, ShopRepository,
                                 ShopStockRepository, UserRepository)
from app.services.order import OrderService
from app.services.product import ProductService
from app.services.sale import SaleService
from app.services.shop import ShopService
from app.services.shop_stock import ShopStockService
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


async def get_sale_repository(
    session: AsyncSession = Depends(get_session)
) -> SaleRepository:
    
    return SaleRepository(session)


async def get_shop_stock_repository(
    session: AsyncSession = Depends(get_session)
) -> ShopStockRepository:

    return ShopStockRepository(session)


async def get_shop_stock_service(
    shop_repository: ShopRepository = Depends(get_shop_repository),
    product_repository: ProductRepository = Depends(get_product_repository),
    shop_stock_repository: ShopStockRepository = Depends(get_shop_stock_repository)
) -> ShopStockService:

    return ShopStockService(shop_repository, product_repository, shop_stock_repository)


async def get_sale_service(
    sale_repository: SaleRepository = Depends(get_sale_repository),
    shop_repository: ShopRepository = Depends(get_shop_repository),
    user_repository: UserRepository = Depends(get_user_repository),
    product_repository: ProductRepository = Depends(get_product_repository),
    shop_stock_service: ShopStockService = Depends(get_shop_stock_service)
) -> SaleService:

    return SaleService(
        sale_repository, shop_repository, user_repository,
        product_repository, shop_stock_service
    )
