from .base import BaseConfig
from pydantic import Field

class AppConfig(BaseConfig):
    APP_TITLE: str = Field(default="AI Animation Platform", description="Application title")
    APP_VERSION: str = Field(default="1.0.0", description="Application version")
    STATIC_DIR: str = Field(default="static", description="Static files directory")
    TEMPLATES_DIR: str = Field(default="templates", description="Templates directory")
    HEALTH_STATUS: str = Field(default="healthy", description="Health check status")
    SERVICE_NAME: str = Field(default="AI Animation Platform", description="Service name") 