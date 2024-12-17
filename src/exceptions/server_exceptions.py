from typing import Self
from fastapi import HTTPException


class ServerError(HTTPException):
    def __init__(
            self: Self,
            detail: str = 'Ошибка сервера',     
            status_code: int = 500,
            headers: dict = None
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            headers=headers
        )


class RabbitMqError(ServerError):
        def __init__(
            self: Self,
            detail: str = 'Ошибка продюсера сообщений',
            status_code: int = 500,
            headers: dict = None
       ):
            super().__init__(
                detail=detail,
                status_code=status_code,
                headers=headers
            )


class DataBaseError(ServerError):
    def __init__(
            self: Self,
            detail: str = 'Ошибка базы данных',
            status_code: int = 500,
            headers: dict = None
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            headers=headers
        )







