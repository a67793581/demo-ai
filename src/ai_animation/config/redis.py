from .base import BaseConfig
from pydantic import Field
import os

class RedisConfig(BaseConfig):
    REDIS_URL: str = Field(default="redis://localhost:6379/0",description="Full Redis URL")
