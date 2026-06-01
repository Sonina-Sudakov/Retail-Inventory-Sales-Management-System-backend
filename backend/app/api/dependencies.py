from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_session
from app.db.repositories import (OrderRepository, ProductRepository,
                                 SaleRepository, ShopRepository,
                                 ShopStockRepository, UserRepository)
from app.db.repositories.shipment import ShipmentRepository
from app.db.repositories.warehouse_stock import WarehouseStockRepository
from app.services.auth import AuthService
from app.services.order import OrderService
from app.services.product import ProductService
from app.services.sale import SaleService
from app.services.shipment import ShipmentService
from app.services.shop import ShopService
from app.services.shop_stock import ShopStockService
from app.services.user import UserService
from app.services.warehouse_stock import WarehouseStockService


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


async def get_warehouse_stock_repository(
    session: AsyncSession = Depends(get_session)
) -> WarehouseStockRepository:

    return WarehouseStockRepository(session)


async def get_warehouse_stock_service(
    warehouse_stock_repository: WarehouseStockRepository = Depends(get_warehouse_stock_repository),
    product_repository: ProductRepository = Depends(get_product_repository)
) -> WarehouseStockService:

    return WarehouseStockService(warehouse_stock_repository, product_repository)


async def get_shipment_repository(
    session: AsyncSession = Depends(get_session)
) -> ShipmentRepository:

    return ShipmentRepository(session)


async def get_shipment_stock_service(
    shipment_repository: ShipmentRepository = Depends(get_shipment_repository),
    shop_repository: ShopRepository = Depends(get_shop_repository),
    user_repository: UserRepository = Depends(get_user_repository),
    product_repository: ProductRepository = Depends(get_product_repository),
    warehouse_stock_service: WarehouseStockService = Depends(get_warehouse_stock_service),
    shop_stock_repository: ShopStockRepository = Depends(get_shop_stock_repository),
    shop_stock_service: ShopStockService = Depends(get_shop_stock_service)
) -> ShipmentService:

    return ShipmentService(
        shipment_repository,
        shop_repository,
        user_repository,
        product_repository,
        warehouse_stock_service,
        shop_stock_repository,
        shop_stock_service
    )


async def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository)
) -> AuthService:

    return AuthService(user_repository)
