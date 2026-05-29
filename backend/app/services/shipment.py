from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.strategy_options import selectinload

from app.db.models.shipment import Shipment
from app.db.models.shipment_item import ShipmentItem
from app.db.repositories.shipment import ShipmentRepository
from app.db.repositories.shop import ShopRepository
from app.db.repositories.user import UserRepository
from app.enums import ShipmentStatus
from app.schemas.shipment import (ShipmentCreate, ShipmentDetailedView,
                                  ShipmentList, ShipmentView)
from app.services.exceptions import (EmptyShipmentError,
                                     ShipmentAlreadyAcceptedError,
                                     ShipmentAlreadyCancelledError,
                                     ShipmentNotFoundError, ShopNotFoundError,
                                     UserNotFoundError)


class ShipmentService:
    def __init__(
            self, 
            session: AsyncSession, 
            shipment_repository: ShipmentRepository, 
            shop_repository: ShopRepository,
            user_repository: UserRepository
        ):
        
        self.session = session
        self.shipment_repository = shipment_repository
        self.shop_repository = shop_repository
        self.user_repository = user_repository


    async def create_shipment(self, schema: ShipmentCreate) -> ShipmentView:
      
        if not schema.items:
            raise EmptyShipmentError()
        
        if schema.to_shop_id is not None:

            shop = await self.shop_repository.get_by_id(schema.to_shop_id)

            if shop is None:
                raise ShopNotFoundError(schema.to_shop_id)

        user = await self.user_repository.get_by_id(schema.created_by_id)

        if user is None:
            raise UserNotFoundError(schema.created_by_id)

        shipment = Shipment(
            from_location=schema.from_location,
            to_shop_id=schema.to_shop_id,
            created_by_id=schema.created_by_id
        )


        async with self.session.begin():
            shipment = await self.shipment_repository.save(shipment)

            for item in schema.items:
                await self.shipment_repository.save_shipment_item(
                    ShipmentItem(
                        shipment_id=shipment.id,
                        product_id=item.product_id,
                        quantity=item.quantity                    
                    )
                )

        return ShipmentView.model_validate(shipment)


    async def get_by_id(self, id: int) -> ShipmentDetailedView:

        shipment = await self.shipment_repository.get_by_id(
            id,
            options=[selectinload(Shipment.items)]
        )
        
        if shipment is None:
            raise ShipmentNotFoundError(id)

        return ShipmentDetailedView.model_validate(shipment)


    async def get_by_shop(self, shop_id: int) -> ShipmentList:

        shipments = await self.shipment_repository.get_shop_shipments(shop_id)
        
        return ShipmentList(
            count=len(shipments),
            items=[ShipmentView.model_validate(shipment) for shipment in shipments]
        )


    async def get_by_status(self, status: ShipmentStatus) -> ShipmentList:

        shipments = await self.shipment_repository.get_shipments_by_status(status)
        
        return ShipmentList(
            count=len(shipments),
            items=[ShipmentView.model_validate(shipment) for shipment in shipments]
        )


    async def get_all(self) -> ShipmentList:

        shipments = await self.shipment_repository.get_all()

        return ShipmentList(
            count=len(shipments),
            items=[ShipmentView.model_validate(shipment) for shipment in shipments]
        )


    async def update_status(self, id: int, status: ShipmentStatus) -> ShipmentView:

        
        shipment = await self.shipment_repository.get_by_id(id)

        if shipment is None:
            raise ShipmentNotFoundError(id)

        shipment.status = status

        async with self.session.begin():
            shipment = await self.shipment_repository.save(shipment)

        return ShipmentView.model_validate(shipment)


    async def accept_shipment(
        self,
        id: int,
        user_id: int
    ) -> ShipmentView:

        shipment = await self.shipment_repository.get_by_id(id)

        if shipment is None:
            raise ShipmentNotFoundError(id)

        user = await self.user_repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError(user_id)

        if shipment.status == ShipmentStatus.CANCELLED:
            raise ShipmentAlreadyCancelledError(id)

        shipment.status = ShipmentStatus.ACCEPTED
        shipment.accepted_by_id = user_id

        async with self.session.begin():
            shipment = await self.shipment_repository.save(shipment)

        return ShipmentView.model_validate(shipment)


    async def cancel_shipment(
        self,
        id: int
    ) -> ShipmentView:

        shipment = await self.shipment_repository.get_by_id(id)

        if shipment is None:
            raise ShipmentNotFoundError(id)

        if shipment.status == ShipmentStatus.ACCEPTED:
            raise ShipmentAlreadyAcceptedError(id)

        shipment.status = ShipmentStatus.CANCELLED

        async with self.session.begin():
            shipment = await self.shipment_repository.save(shipment)

        return ShipmentView.model_validate(shipment)
