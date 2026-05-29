from datetime import datetime

from sqlalchemy import CheckConstraint, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base


class ShopStock(Base):
    __tablename__ = 'shop_stocks'

    product_id: Mapped[int] = mapped_column(
        ForeignKey('products.id'),
        primary_key=True
    )

    product: Mapped['Product'] = relationship( 
        lazy='raise'
    )

    shop_id: Mapped[int] = mapped_column(
        ForeignKey('shops.id'),
        primary_key=True
    )

    shop: Mapped['Shop'] = relationship(
        lazy='raise'
    )

    quantity: Mapped[int] = mapped_column(
        CheckConstraint('quantity >= 0'),
        nullable=False
    )

    min_quantity: Mapped[int] = mapped_column(
        CheckConstraint('min_quantity >= 0'),
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
