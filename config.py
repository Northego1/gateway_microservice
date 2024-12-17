import os
from pathlib import Path
from typing import Self
from pydantic import BaseModel

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[0]



class RabbitMQSettings:
    def __init__(self):  
        self.RMQ_HOST = os.getenv('RMQ_HOST')
        self.RMQ_PORT = os.getenv('RMQ_PORT')
        self.RMQ_USER = os.getenv('RMQ_USER')
        self.RMQ_PASSWORD = os.getenv('RMQ_PASSWORD')

    @property
    def rabbit_mq_dsn(self: Self) -> str:
        return f"amqp://{self.RMQ_USER}:{self.RMQ_PASSWORD}@{self.RMQ_HOST}/"


class AuthJwtSettings(BaseModel):
    algorithm: str = "RS256"
    type_field: str = "type"
    access_type: str = "access"
    refresh_type: str = "refresh"

    refresh_expire: int = 43200 # minutes (30 days)
    access_expire: int = 10 # minutes

    max_user_sessions: int = 5


class Settings:
    def __init__(self: Self, env_file_name: str):
        env_path = os.path.join(BASE_DIR, env_file_name)
        load_dotenv(env_path, override=True)

    rmq: RabbitMQSettings = RabbitMQSettings()
    jwt: AuthJwtSettings = AuthJwtSettings()
    

settings = Settings(env_file_name='.env')