from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    ) 