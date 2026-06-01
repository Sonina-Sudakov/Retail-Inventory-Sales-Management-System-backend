from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base


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
        lazy='raise'
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
        nullable=False
    )

    user: Mapped['User'] = relationship(
        lazy='raise'
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False
    )

    items: Mapped[list['SaleItem']] = relationship(
        back_populates='sale',
        cascade='all, delete-orphan',
        lazy='raise'
    )
