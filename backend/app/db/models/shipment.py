from datetime import datetime

from base import Base
from enums import ShipmentFromLocation, ShipmentStatus
from sqlalchemy import Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Shipment(Base):
    __tablename__ = "shipments"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    from_location: Mapped[str] = mapped_column(
        Enum(ShipmentFromLocation),
        nullable=False
    )

    to_shop_id: Mapped[int | None] = mapped_column(
        ForeignKey('shops.id'),
        nullable=True
    )

    to_shop: Mapped['Shop | None'] = relationship(
        lazy='raise'
    )

    status: Mapped[str] = mapped_column(
        Enum(ShipmentStatus),
        default = ShipmentStatus.CREATED,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), 
        onupdate=func.now(),
        nullable=False
    )

    created_by_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
        nullable=False
    )

    created_by: Mapped['User'] = relationship( 
        lazy='raise'
    )

    accepted_by_id: Mapped[int | None] = mapped_column(
        ForeignKey('users.id'),
        nullable=True
    )

    accepted_by: Mapped['User | None'] = relationship( 
        lazy='raise'
    )

    shipment_items: Mapped[list['ShipmentItem']] = relationship(
        back_populates='shipment',
        lazy='raise'
    )
