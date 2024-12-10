
from pathlib import Path
from typing import LiteralString, Self

from pydantic import BaseModel


BASE_DIR = Path(__file__).resolve().parents[1]
class RabbitMQSettings:
    RMQ_HOST = "0.0.0.0"
    RMQ_PORT = 5672
    RMQ_USER = "guest"
    RMQ_PASSWORD = "guest"

    MQ_EXCHANGE = ""
    MQ_ROUTING_KEY = "news"
    MQ_START_CHANNEL_POOL = 1

    @property
    def rabbit_mq_dsn(self: Self) -> LiteralString:
        return f"amqp://{self.RMQ_USER}:{self.RMQ_PASSWORD}@{self.RMQ_HOST}/"
    

class AuthJwt(BaseModel):
    type_field: str = "type"
    access_type: str = "access"
    refresh_type: str = "refresh"

    refresh_expire: int = 43200 # 30 days
    access_expire: int = 10

    max_user_sessions: int = 5


class Prometheus(BaseModel):
    HOST: str = 'localhost'
    PORT: int = 9090


class Settings:
    rmq: RabbitMQSettings = RabbitMQSettings()
    jwt: AuthJwt = AuthJwt()
    prometheus = Prometheus()


settings = Settings()