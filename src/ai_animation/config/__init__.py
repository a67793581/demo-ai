from .db import DBConfig
from .api import APIConfig
from .app import AppConfig
from .redis import RedisConfig
from .task import TaskConfig
from .error import ErrorConfig

class Settings:
    """Aggregated settings class providing access to all configuration modules"""
    db = DBConfig()
    api = APIConfig()
    app = AppConfig()
    redis = RedisConfig()
    task = TaskConfig()
    error = ErrorConfig()

settings = Settings()

__all__ = ["settings"] 