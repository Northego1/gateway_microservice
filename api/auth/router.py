
from fastapi import (
    APIRouter
)
from schemas import api_responses
from api.auth.v1 import controllers


router = APIRouter(
    tags=['Auth'],
    prefix='/v1/auth',
    responses={
        203: {"model": api_responses.DefaultResponse},
        401: {"model": api_responses.DefaultResponse},
        403: {"model": api_responses.DefaultResponse},
        422: {"model": api_responses.ValidationResponse422}
    },
)


@router.post(
        '/login',
        status_code=201,
        response_model_exclude_none=True,
        responses={201: {"model": api_responses.ApiReponseLogin}},
)
async def login(
    LoginUserController: controllers.LoginUserController
) -> api_responses.ApiReponseLogin:
    response_schema = await LoginUserController.login_user()
    
    return response_schema


@router.post(
        '/register',
        response_model_exclude_none=True,
)
async def register(
    RegisterUserController: controllers.RegisterUserController
) -> api_responses.DefaultResponse:
    response_schema = await RegisterUserController.register_user()
    return response_schema


@router.post(
        '/refresh',
        response_model_exclude_none=True,
)
async def refresh_jwt(
    RefreshTokenController: controllers.RefreshTokenController
) -> api_responses.RefreshResponseAccess:
    response_schema = await RefreshTokenController.refresh_access_token()

    return response_schema


@router.post(
        '/logout',
        status_code=203,
        response_model_exclude_none=True
)
async def logout(
    LogoutUserController: controllers.LogoutUserController
) -> api_responses.DefaultResponse:
    response_schema = await LogoutUserController.logout_user()
    return response_schema




