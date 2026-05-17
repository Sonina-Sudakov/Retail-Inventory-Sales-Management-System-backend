from datetime import datetime

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from base import Base


class Sale(Base):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    shop_id: Mapped[int] = mapped_column(
        ForeignKey('shops.id'),
        nullable=False
    )

    shop: Mapped['Shop'] = relationship( 
        back_populates='sales'
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
        nullable=False
    )

    user: Mapped['User'] = relationship(
        back_populates='sales'
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False
    )

    sale_items: Mapped[list['SaleItem']] = relationship(
        back_populates='sale'
    )
