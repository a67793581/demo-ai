"""
Core business logic module for AI Animation Platform
"""

from ai_animation.storage.storage import storage
from .tasks import process_animation_task

__all__ = ['storage', 'process_animation_task'] 