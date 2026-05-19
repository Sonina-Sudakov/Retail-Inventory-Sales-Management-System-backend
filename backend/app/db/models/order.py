from datetime import datetime

from base import Base
from enums import OrderStatus
from sqlalchemy import Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Order(Base):
    __tablename__ = 'orders'

    id : Mapped[int] = mapped_column(
        primary_key=True
    )

    to_shop_id: Mapped[int] = mapped_column(
        ForeignKey('shops.id'),
        nullable=False
    )

    to_shop: Mapped['Shop'] = relationship(
        lazy='raise'
    )

    status: Mapped[str] = mapped_column(
        Enum(OrderStatus),
        default=OrderStatus.PENDING,
        nullable=False
    )

    accepted_at: Mapped[datetime | None] = mapped_column(
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False
    )

    order_items: Mapped[list['OrderItem']] = relationship(
        back_populates='order',
        lazy='raise'
    )
