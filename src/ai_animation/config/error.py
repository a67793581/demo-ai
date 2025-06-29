from .base import BaseConfig
from pydantic import Field

class ErrorConfig(BaseConfig):
    ERROR_AI_SERVICE_UNAVAILABLE: str = "AI服务暂时不可用，请稍后重试"
    ERROR_OCR_FAILED: str = "OCR识别失败：图片质量过低或格式不支持"
    ERROR_PROMPT_FAILED: str = "提示词生成失败：输入内容包含敏感信息"
    ERROR_VIDEO_FAILED: str = "视频生成失败：服务器资源不足，请稍后重试" 