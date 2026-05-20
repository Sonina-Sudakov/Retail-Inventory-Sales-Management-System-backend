from enum import Enum


class UserRole(str, Enum):
    ADMIN = 'ADMIN'
    STOREKEEPER = 'STOREKEEPER'
    SHOPKEEPER = 'SHOPKEEPER'


class OrderStatus(str, Enum):
    PENDING = 'PENDING'
    ACCEPTED = 'ACCEPTED'
    CANCELED = 'CANCELED'


class ShipmentStatus(str, Enum):
    CREATED = 'CREATED'
    IN_DELIVERY = "IN_DELIVERY"
    CANCELED = 'CANCELED'
    ACCEPTED = 'ACCEPTED'


class ShipmentFromLocation(str, Enum):
    SUPPLIER = 'SUPPLIER'
    WAREHOUSE = 'WAREHOUSE'
