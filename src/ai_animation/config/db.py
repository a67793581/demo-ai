from .base import BaseConfig
from pydantic import Field
import os

class DBConfig(BaseConfig):
    MONGO_URI: str = Field(default="mongodb://localhost:27017/", description="MongoDB connection URI")
    MONGO_DATABASE: str = Field(default="ai_animation", description="MongoDB database name")
    MONGO_COLLECTION: str = Field(default="tasks", description="MongoDB collection name")
    CONNECTION_TIMEOUT: int = Field(default=5000, description="MongoDB connection timeout in milliseconds")
    
    # MongoDB认证配置
    MONGO_USERNAME: str = Field(default="admin", description="MongoDB username")
    MONGO_PASSWORD: str = Field(default="password", description="MongoDB password")
    MONGO_AUTH_DATABASE: str = Field(default="admin", description="MongoDB authentication database")
