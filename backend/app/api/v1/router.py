from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.order import router as order_router
from app.api.v1.product import router as product_router
from app.api.v1.sale import router as sale_router
from app.api.v1.shipment import router as shipment_router
from app.api.v1.shop import router as shop_router
from app.api.v1.user import router as user_router
from app.api.v1.warehouse import router as warehouse_router

router = APIRouter(prefix='/v1')

router.include_router(order_router)
router.include_router(product_router)
router.include_router(sale_router)
router.include_router(shipment_router)
router.include_router(shop_router)
router.include_router(user_router)
router.include_router(warehouse_router)
router.include_router(auth_router)
