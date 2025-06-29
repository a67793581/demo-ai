"""
AI Animation Platform

A FastAPI + Celery + Redis + MongoDB platform for AI-powered animation generation.
"""

from .api import router
from .storage.storage import storage
from .core import process_animation_task
from .config import settings

__version__ = "1.0.0"
__all__ = [
    'router',
    'storage', 
    'process_animation_task',
    'settings'
] 