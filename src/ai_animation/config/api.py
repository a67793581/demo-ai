from .base import BaseConfig
from pydantic import Field
from typing import List

class APIConfig(BaseConfig):
    API_PREFIX: str = Field(default="/ai-animation", description="API route prefix")
    API_TAGS: List[str] = Field(default=["AI Animation"], description="API documentation tags")
    TASK_ID_SEPARATOR: str = Field(default="_", description="Task ID separator")
    TASK_ID_SUFFIX_LENGTH: int = Field(default=8, description="Task ID suffix length") 