from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.api.dependencies import get_user_service
from app.schemas.user import (UserCreate, UserList, UserUpdateFullname,
                              UserUpdatePassword, UserView)
from app.services.user import UserService

router = APIRouter(prefix='/users')


@router.post('/', response_model=UserView)
async def create_user(
    user: UserCreate,
    user_service: UserService = Depends(get_user_service)
):

    return await user_service.create(user)


@router.get('/{id}', response_model=UserView)
async def get_user_by_id(
    id: int,
    user_service: UserService = Depends(get_user_service)
):

    return await user_service.get_by_id(id)


@router.delete('/{id}')
async def delete_user_by_id(
    id: int,
    user_service: UserService = Depends(get_user_service)
):

    await user_service.delete(id)

    return JSONResponse(content={'message' : 'User is succesfully deleted'}, status_code=200)


@router.get('/all', response_model=UserList)
async def get_all_users(
    user_service: UserService = Depends(get_user_service)
):

    return await user_service.get_all()


@router.put('/change_password', response_model=UserView)
async def change_password(
    schema: UserUpdatePassword,
    user_service: UserService = Depends(get_user_service)
):

    return await user_service.change_password(schema)


@router.put('/change_fullname', response_model=UserView)
async def change_fullname(
    schema: UserUpdateFullname,
    user_service: UserService = Depends(get_user_service)
):

    return await user_service.change_fullname(schema)
