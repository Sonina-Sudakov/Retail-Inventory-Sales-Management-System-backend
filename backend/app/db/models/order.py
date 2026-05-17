from datetime import datetime

from base import Base
from sqlalchemy import Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from enums import OrderStatus


class Order(Base):
    __tablename__ = 'orders'

    id : Mapped[int] = mapped_column(
        primary_key=True
    )

    shop_id: Mapped[int] = mapped_column(
        ForeignKey('shops.id'),
        nullable=False
    )

    shop: Mapped['Shop'] = relationship(
        back_populates='orders'
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

    order_items: Mapped[list['OrderItems']] = relationship(
        back_populates='order'
    )
