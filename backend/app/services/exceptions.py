class UserNotFoundError(Exception):
    def __init__(self, user_id: int):
        self.user_id = user_id


class UserAlreadyExistsError(Exception):
    def __init__(self, username: str):
        self.username = username


class ProductNotFoundError(Exception):
    def __init__(self, product_id: int):
        self.product_id = product_id


class ProductAlreadyExistsError(Exception):
    def __init__(self, name: str):
        self.name = name


class ShopNotFoundError(Exception):
    def __init__(self, shop_id: int):
        self.shop_id = shop_id


class ShopAlreadyExistsError(Exception):
    def __init__(self, phone_number: str, email: str):
        self.phone_number = phone_number
        self.email = email


class SaleNotFoundError(Exception):
    def __init__(self, sale_id: int):
        self.sale_id = sale_id


class EmptySaleError(Exception):
    def __init__(self):
        super().__init__(
            "Sale must contain at least one item"
        )

class OrderNotFoundError(Exception):
    def __init__(self, order_id: int):
        self.order_id = order_id


class OrderIsNotPendingError(Exception):
    def __init__(self, order_id: int):
        self.order_id = order_id


class EmptyOrderError(Exception):
    def __init__(self):
        super().__init__(
            "Order must contain at least one item"
        )


class ShipmentNotFoundError(Exception):
    def __init__(self, shipment_id: int):
        self.shipment_id = shipment_id


class EmptyShipmentError(Exception):
    def __init__(self):
        super().__init__(
            "Shipment must contain at least one item"
        )


class ShipmentAlreadyAcceptedError(Exception):
    def __init__(self, shipment_id: int):
        super().__init__(
            "Shipment is already accepted and cannot be canceled"
        )
        self.shipment_id = shipment_id


class ShipmentAlreadyCanceledError(Exception):
    def __init__(self, shipment_id: int):
        super().__init__(
            "Shipment is already canceled and cannot be accepted"
        )
        self.shipment_id = shipment_id


class ShopStockNotFoundError(Exception):
    def __init__(self, shop_id, product_id):
        self.shop_id = shop_id
        self.product_id = product_id


class InsufficientShopStockError(Exception):
    def __init__(self, shop_id, product_id, quantity, change):
        self.shop_id = shop_id
        self.product_id = product_id
        self.quantity = quantity 
        self.change = change 


class InvalidQuantityError(Exception):
    def __init__(self, quantity):
        self.quantity = quantity


class InvalidMinQuantityError(Exception):
    def __init__(self, min_quantity):
        self.min_quantity = min_quantity


class WarehouseStockAlreadyExistsError(Exception):
    def __init__(self, cell_code):
        self.cell_code = cell_code


class WarehouseStockNotFoundError(Exception):
    def __init__(self, id):
        self.id = id


class WarehouseStockWithProductNotFoundError(Exception):
    def __init__(self, id):
        self.id = id


class InsufficientWarehouseStockError(Exception):
    def __init__(self, id, quantity, change):
        self.id = id 
        self.quantity = quantity
        self.change = change 


class InvalidChangeValueError(Exception):
    def __init__(self, change):
        self.change = change


class DuplicateCellCodeError(Exception):
    def __init__(self, cell_code):
        self.cell_code = cell_code


class InvalidCredentialsError(Exception):
    def __init__(self):
        pass


class UnauthorizedError(Exception):
    def __init__(self):
        pass


class ForbiddenError(Exception):
    def __init__(self):
        pass
