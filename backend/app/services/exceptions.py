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
    def __init__(self, phone_number: str):
        self.phone_number = phone_number
