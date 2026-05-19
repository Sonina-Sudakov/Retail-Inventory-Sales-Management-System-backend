from app.db.models.shipment import Shipment
from app.db.repositories.base_repository import BaseRepository
from enums import ShipmentStatus
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select


class ShipmentRepository(
    BaseRepository[Shipment]
):
    def __init__(
        self,
        session: AsyncSession
    ):
        super().__init__(Shipment, session)


    async def get_shop_shipments(
        self,
        shop_id: int
    ) -> list[Shipment]:
        
        stmt = select(Shipment).where(Shipment.to_shop_id == shop_id)

        result = await self.session.execute(stmt)

        return list(result.scalars().all())

   
    async def get_shipments_by_status(
        self,
        status: ShipmentStatus
    ) -> list[Shipment]:

        stmt = select(Shipment).where(Shipment.status == status)

        result = await self.session.execute(stmt)

        return list(result.scalars().all())        
