from datetime import datetime

from base import Base
from sqlalchemy import CheckConstraint, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ShopStock(Base):
    __tablename__ = 'shopStocks'

    product_id: Mapped[int] = mapped_column(
        ForeignKey('products.id'),
        primary_key=True
    )

    product: Mapped['Product'] = relationship( 
        back_populates='shop_stocks'
    )

    shop_id: Mapped[int] = mapped_column(
        ForeignKey('shops.id'),
        primary_key=True
    )

    shop: Mapped['Shop'] = relationship(
        back_populates='shop_stocks'
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
