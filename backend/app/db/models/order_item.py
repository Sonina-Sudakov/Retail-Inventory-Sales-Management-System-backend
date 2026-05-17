from base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class OrderItem(Base):
    __tablename__ = 'orderItems'    

    order_id: Mapped[int] = mapped_column(
        ForeignKey('orders.id'),
        primary_key=True
    )

    order: Mapped['Order'] = relationship(
        back_populates='order_items'
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey('products.id'),
        primary_key=True
    )

    product: Mapped['Product'] = relationship( 
        back_populates='order_items'
    )

    quantity: Mapped[int] = mapped_column(
        nullable=False
    )
