from fastapi import APIRouter, Depends

from app.api.dependencies import get_shipment_stock_service
from app.core.auth.dependencies import get_current_user, require_role
from app.enums import ShipmentStatus, UserRole
from app.schemas.shipment import (ShipmentCreate, ShipmentDetailedView,
                                  ShipmentList, ShipmentView)
from app.services.shipment import ShipmentService

router = APIRouter(prefix='/shipments')


@router.post('/', response_model=ShipmentView)
async def create_shipment(
    schema: ShipmentCreate,
    shipment_service: ShipmentService = Depends(get_shipment_stock_service),
    user=Depends(
        require_role(UserRole.STOREKEEPER)
    )
):

    return await shipment_service.create_shipment(schema)


@router.get('/', response_model=ShipmentDetailedView)
async def get_shipment(
    id: int,
    shipment_service: ShipmentService = Depends(get_shipment_stock_service),
    user=Depends(
        require_role(UserRole.ADMIN, UserRole.STOREKEEPER)
    )
):

    return await shipment_service.get_by_id(id)


@router.get('/all', response_model=ShipmentList)
async def get_all(
    shipment_service: ShipmentService = Depends(get_shipment_stock_service),
    user=Depends(
        require_role(UserRole.ADMIN, UserRole.STOREKEEPER)
    )
):

    return await shipment_service.get_all()


@router.get('/shop', response_model=ShipmentList)
async def get_shop_shipments(
    id: int,
    shipment_service: ShipmentService = Depends(get_shipment_stock_service),
    user=Depends(
        get_current_user
    )
):

    return await shipment_service.get_by_shop(id)


@router.get('/status', response_model=ShipmentList)
async def get_shipments_by_status(
    status: ShipmentStatus,
    shipment_service: ShipmentService = Depends(get_shipment_stock_service),
    user=Depends(
        get_current_user
    )
):

    return await shipment_service.get_by_status(status)


@router.put('/accept', response_model=ShipmentView)
async def accept_shipment(
    shipment_id: int,
    user_id: int,
    shipment_service: ShipmentService = Depends(get_shipment_stock_service),
    user=Depends(
        require_role(UserRole.SHOPKEEPER, UserRole.STOREKEEPER)
    )
):

    return await shipment_service.accept_shipment(shipment_id, user_id)


@router.put('/cancel', response_model=ShipmentView)
async def cancel_shipment(
    shipment_id: int,
    shipment_service: ShipmentService = Depends(get_shipment_stock_service),
    user=Depends(
        require_role(UserRole.SHOPKEEPER, UserRole.STOREKEEPER)
    )
):

    return await shipment_service.cancel_shipment(shipment_id)
