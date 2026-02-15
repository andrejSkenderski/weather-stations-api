from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from config.container import Container
from models.dtos.requests import LoginRequest
from services.auth import JwtAuthenticator

auth_api = APIRouter(prefix="/auth", tags=["Auth"])

bearer_scheme = HTTPBearer()


@auth_api.post("/login", response_model=None, summary="Authenticate user")
@inject
async def login(
        request: LoginRequest,
        auth_service: JwtAuthenticator = Depends(Provide[Container.jwt_auth]),
):
    return auth_service.authenticate_user(request)


@auth_api.post("/logout", response_model=None, summary="Logout user")
@inject
async def logout(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        auth_service: JwtAuthenticator = Depends(Provide[Container.jwt_auth]),
):
    return auth_service.logout(credentials.credentials)


@inject
async def verify_token(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        auth_service: JwtAuthenticator = Depends(Provide[Container.jwt_auth]),
) -> dict:
    return auth_service.verify_token(credentials.credentials)
