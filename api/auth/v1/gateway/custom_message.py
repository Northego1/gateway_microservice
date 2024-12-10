from typing import Self, Union
import uuid
from aio_pika import Message
from pydantic import BaseModel

import pickle


class CustomMessage(Message):
    def __init__(
            self: Self,
            body: dict | BaseModel,
            correlation_id: str = None,
            **kwargs
    ):
        payload = self._convert(body)
        super().__init__(body=payload, correlation_id=correlation_id, **kwargs)



    def _convert(self: Self, body: dict | BaseModel) -> bytes:
        if isinstance(body, BaseModel):
            return pickle.dumps(body.model_dump())
        else: 
            return pickle.dumps(body)



