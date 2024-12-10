import hashlib
from typing import Self

from fastapi import Request

from exceptions.client_exceptions import ClientError




def extract_fingerprint_and_hash(request: Request) -> bytes:
    user_agent = request.headers.get('user-agent')
    if not user_agent:
        raise ClientError('Ошибка заголовков запроса')
    hash_value = hashlib.sha256(user_agent.encode()).digest()
    return hash_value