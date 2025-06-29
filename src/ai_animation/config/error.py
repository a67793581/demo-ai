from .base import BaseConfig
from pydantic import Field

class ErrorConfig(BaseConfig):
    ERROR_AI_SERVICE_UNAVAILABLE: str = "AI service temporarily unavailable"
    ERROR_OCR_FAILED: str = "OCR recognition failed: image quality too low or format not supported"
    ERROR_PROMPT_FAILED: str = "Prompt generation failed: input contains sensitive content"
    ERROR_VIDEO_FAILED: str = "Video generation failed: insufficient server resources, please try again later" 