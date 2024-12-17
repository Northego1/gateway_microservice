from contextlib import asynccontextmanager

from pydantic import ValidationError
from api import auth
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


from schemas import api_responses
from exceptions.client_exceptions import ClientError
from exceptions.server_exceptions import ServerError
from api.auth.v1.gateway.rabbit_mq_setup import rabbit_mq_setup, shutdown


@asynccontextmanager
async def lifespan(app: FastAPI):
    await rabbit_mq_setup()
    yield
    await shutdown()

app = FastAPI(lifespan=lifespan)
app.include_router(router=auth.auth_router)




@app.exception_handler(ClientError)
async def auth_exception_handler(
    request: Request,
    exc: ClientError
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=api_responses.DefaultResponse(
            status_code=exc.status_code,
            detail=exc.detail
        ).model_dump()
    )


@app.exception_handler(ServerError)
async def auth_exception_handler(
    request: Request,
    exc: ServerError
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=api_responses.DefaultResponse(
            status_code=exc.status_code,
            detail=exc.detail
        ).model_dump()
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content=api_responses.ValidationResponse422(
            status_code=422,
            detail=exc.errors(),
        ).model_dump()
    )


@app.exception_handler(ValidationError)
async def pydantic_validation_exception_handler(
    request: Request,
    exc: ValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content=api_responses.ValidationResponse422(
            status_code=422,
            detail=exc.errors(),
        ).model_dump()
    )
