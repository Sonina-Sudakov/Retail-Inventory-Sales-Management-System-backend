from fastapi import Request
from fastapi.responses import JSONResponse

from app.services.exceptions import (UserAlreadyExistsError, UserNotFoundError,
                                     UserPasswordsMismatchError)


async def user_not_found_handler(
    request: Request,
    exc: UserNotFoundError
):

    return JSONResponse(
        status_code=404,
        content={
            "message":
                f"User with id = {exc.user_id} doesn't exist"
        }
    )


async def user_already_exists_handler(
    request: Request,
    exc: UserAlreadyExistsError
):

    return JSONResponse(
        status_code=409,
        content={
            "message":
                f"User with username = {exc.username} already exists"
        }
    )


async def passwords_mismatch_handler(
    request: Request,
    exc: UserPasswordsMismatchError
):

    return JSONResponse(
        status_code=422,
        content={
            "message":
                f"Wrong old password for user {exc.username}"
        }
    )
