from app.api.dependencies import get_user_service
from app.schemas.user import (UserCreate, UserList, UserUpdateFullname,
                              UserUpdatePassword, UserView)
from app.services.exceptions import (UserAlreadyExistsError, UserNotFoundError,
                                     UserPasswordsMismatchError)
from app.services.user import UserService
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

router = APIRouter(prefix='/users')


@router.post('/', response_model=UserView)
async def create_user(
    user: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    try:
        return await user_service.create(user)
    except UserAlreadyExistsError:
        return JSONResponse(
            content={'message': f'User with username={user.username} already exists'},
            status_code=409
        )


@router.get('/{id}', response_model=UserView)
async def get_user_by_id(
    id: int,
    user_service: UserService = Depends(get_user_service)
):
    try:
        return await user_service.get_by_id(id)
    except UserNotFoundError:
        return JSONResponse(content={'message': f'User with id={id} doesn\'t exist'}, status_code=404)


@router.delete('/{id}')
async def delete_user_by_id(
    id: int,
    user_service: UserService = Depends(get_user_service)
):

    try:
        await user_service.delete(id)
    except UserNotFoundError:
        return JSONResponse(content={'message': f'User with id={id} doesn\'t exist'}, status_code=404)

    return JSONResponse(content={'message' : 'User is succesfully deleted'}, status_code=404)


@router.get('/', response_model=UserList)
async def get_all_users(
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_all()


@router.put('/change_password', response_model=UserView)
async def change_password(
    schema: UserUpdatePassword,
    user_service: UserService = Depends(get_user_service)
):
    try:
        return await user_service.change_password(schema)
    except UserNotFoundError as err:
        return JSONResponse(content={'message': f'User with id={err.user_id} doesn\'t exist'}, status_code=404)
    except UserPasswordsMismatchError as err:
        return JSONResponse(content={'message': f'Wrong old password for user {err.username}'}, status_code=422)


@router.put('/change_fullname', response_model=UserView)
async def change_fullname(
    schema: UserUpdateFullname,
    user_service: UserService = Depends(get_user_service)
):
    try:
        return await user_service.change_fullname(schema)
    except UserNotFoundError as err:
        return JSONResponse(content={'message': f'User with id={err.user_id} doesn\'t exist'}, status_code=404)
