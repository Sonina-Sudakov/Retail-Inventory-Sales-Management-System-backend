from datetime import datetime

from base import Base
from enums import UserRole
from sqlalchemy import Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    username: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False
    )

    fullname: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    hash_password: Mapped[str] = mapped_column(
        String(60),
        nullable=False
    )

    role: Mapped[str] = mapped_column(
        Enum(UserRole),
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

    sales: Mapped[list['Sale']] = relationship(
        back_populates='user',
        lazy='raise'
    )

    created_shipments: Mapped[list['Shipment']] = relationship(
        back_populates='created_by',
        lazy='raise'
    )

    accepted_shipments: Mapped[list['Shipment']] = relationship(
        back_populates='accepted_by',
        lazy='raise'
    )
