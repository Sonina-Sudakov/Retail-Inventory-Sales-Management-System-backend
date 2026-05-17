from datetime import datetime

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from base import Base


class Shop(Base):
    __tablename__ = 'shops'

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(60),
        nullable=False
    )

    address: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    contact_face: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    phone_number: Mapped[str] = mapped_column(
        String(16),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(60),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), 
        onupdate=func.now(),
        nullable=False
    )

    orders: Mapped[list['Order']] = relationship(
        back_populates='shop'
    )
