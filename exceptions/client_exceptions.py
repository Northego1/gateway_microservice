from typing import Self
from fastapi import HTTPException


class ClientError(HTTPException):
    def __init__(
            self: Self,
            detail: str = 'Неизвестная ошибка',            
            status_code: int = 400,
            headers: dict = None
    ):
        super().__init__(status_code, detail, headers)


class AuthError(ClientError):
    def __init__(
            self: Self,
            detail: str = 'Ошибка аутентификации',
            status_code: int = 401,
            headers: dict = None
    ):
        super().__init__(detail, status_code, headers)


class JwtError(ClientError):
    def __init__(
            self: Self,
            detail: str = 'Ошибка токен-сервиса',
            status_code: int = 400,
            headers: dict = None
    ):
        super().__init__(detail, status_code, headers)


class FingerprintError(ClientError):
    def __init__(
            self: Self,
            detail: str = 'Неизвестная ошибка',
            status_code: int = 403,
            headers: dict = None
    ):
        super().__init__(detail, status_code, headers)


