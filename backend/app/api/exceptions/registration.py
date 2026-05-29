from fastapi import FastAPI

from app.api.exceptions.handlers import (passwords_mismatch_handler,
                                         user_already_exists_handler,
                                         user_not_found_handler)
from app.services.exceptions import (UserAlreadyExistsError, UserNotFoundError,
                                     UserPasswordsMismatchError)


def register_exception_handlers(app: FastAPI):

    app.add_exception_handler(
        UserNotFoundError,
        user_not_found_handler
    )

    app.add_exception_handler(
        UserAlreadyExistsError,
        user_already_exists_handler
    )

    app.add_exception_handler(
        UserPasswordsMismatchError,
        passwords_mismatch_handler
    )
