from datetime import datetime

from sqlalchemy import Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base
from app.enums import ShipmentFromLocation, ShipmentStatus


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
        foreign_keys=[created_by_id],
        lazy='raise'
    )

    accepted_by_id: Mapped[int | None] = mapped_column(
        ForeignKey('users.id'),
        nullable=True
    )

    accepted_by: Mapped['User | None'] = relationship( 
        foreign_keys=[accepted_by_id],
        lazy='raise'
    )

    items: Mapped[list['ShipmentItem']] = relationship(
        back_populates='shipment',
        lazy='raise'
    )
