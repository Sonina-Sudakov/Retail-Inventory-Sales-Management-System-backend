from fastapi import APIRouter, Depends

from app.api.dependencies import get_order_service
from app.core.auth.dependencies import get_current_user, require_role
from app.enums import OrderStatus, UserRole
from app.schemas.order import (OrderCreate, OrderDetailedView, OrderList,
                               OrderView)
from app.services.order import OrderService

router = APIRouter(prefix='/orders')

@router.post('/', response_model=OrderView)
async def create_order(
    order: OrderCreate,
    order_service: OrderService = Depends(get_order_service),
    user=Depends(
        require_role(UserRole.SHOPKEEPER)
    )
):

    return await order_service.create_order(order)


@router.get('/', response_model=OrderDetailedView)
async def get_order_by_id(
    id: int,
    order_service: OrderService = Depends(get_order_service),
    user=Depends(
        get_current_user
    )
):

    return await order_service.get_by_id(id)


@router.get('/all', response_model=OrderList)
async def get_all_orders(
    order_service: OrderService = Depends(get_order_service),
    user=Depends(
        get_current_user
    )
):

    return await order_service.get_all()


@router.get('/shop/{shop_id}', response_model=OrderList)
async def get_shop_orders(
    shop_id: int,
    order_service: OrderService = Depends(get_order_service),
    user=Depends(
        get_current_user
    )
):

    return await order_service.get_by_shop(shop_id)


@router.get('/status', response_model=OrderList)
async def get_orders_by_status(
    status: OrderStatus, 
    order_service: OrderService = Depends(get_order_service),
    user=Depends(
        get_current_user
    )
):
    return await order_service.get_by_status(status)


@router.put('/{id}/accept', response_model=OrderView)
async def accept_order(
    id: int,
    order_service: OrderService = Depends(get_order_service),
    user=Depends(
        require_role(UserRole.STOREKEEPER)
    )
):
    return await order_service.accept_order(id)


@router.put('/{id}/cancel', response_model=OrderView)
async def cancel_order(
    id: int,
    order_service: OrderService = Depends(get_order_service),
    user=Depends(
        require_role(UserRole.STOREKEEPER, UserRole.SHOPKEEPER)
    )
):
    return await order_service.cancel_order(id)
