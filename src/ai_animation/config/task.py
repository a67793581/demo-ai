from .base import BaseConfig
from pydantic import Field

class TaskConfig(BaseConfig):
    TASK_STATUS_QUEUED: str = "queued"
    TASK_STATUS_PROCESSING: str = "processing"
    TASK_STATUS_FINISHED: str = "finished"
    TASK_STATUS_FAILED: str = "failed"

    INPUT_TYPE_TEXT: str = "text"
    INPUT_TYPE_IMAGE: str = "image"

    DEFAULT_PAGE: int = 1
    DEFAULT_PAGE_SIZE: int = 10

    TASK_PROCESSING_TIME: int = Field(default=3, description="Task processing time in seconds")
    SUCCESS_RATE: float = Field(default=0.8, description="Task success rate (0.0-1.0)")
    OCR_FAILURE_RATE: float = Field(default=0.1, description="OCR failure rate (0.0-1.0)")
    PROMPT_FAILURE_RATE: float = Field(default=0.05, description="Prompt generation failure rate (0.0-1.0)")
    VIDEO_FAILURE_RATE: float = Field(default=0.15, description="Video generation failure rate (0.0-1.0)")

    VIDEO_URL_TEMPLATE: str = "https://localhost:8000/static/generated-video-{video_id}.mp4"
    TASK_SUCCESS_MESSAGE: str = Field(default="Task completed successfully", description="Task success message") 