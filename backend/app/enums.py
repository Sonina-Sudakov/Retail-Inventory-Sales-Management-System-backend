from enum import Enum


class UserRole(str, Enum):
    ADMIN = 'ADMIN'
    STOREKEEPER = 'STOREKEEPER'
    SHOPKEEPER = 'SHOPKEEPER'

class OrderStatus(str, Enum):
    PENDING = 'PENDING'
    ACCEPTED = 'ACCEPTED'
    CANCELED = 'CANCELED'
