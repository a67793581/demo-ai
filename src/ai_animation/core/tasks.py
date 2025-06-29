from test.celery_app import celery_app
from ai_animation.storage.storage import storage
from ..config import settings
import time
import random
import uuid
from datetime import datetime

task_cfg = settings.task
error_cfg = settings.error

@celery_app.task
def process_animation_task(task_id: str, user_id: str, input_type: str, input_content: str):
    """Process animation generation task with OCR, prompt generation, and video API"""
    try:
        storage.update_task(task_id, status=task_cfg.TASK_STATUS_PROCESSING)
        
        # Simulate processing time
        time.sleep(task_cfg.TASK_PROCESSING_TIME)
        
        # Simulate task success/failure
        if random.random() > task_cfg.SUCCESS_RATE:
            raise Exception(error_cfg.ERROR_AI_SERVICE_UNAVAILABLE)
        
        # Extract text content
        text_content = perform_ocr(input_content) if input_type == task_cfg.INPUT_TYPE_IMAGE else input_content
        
        # Generate prompt
        prompt = generate_prompt(text_content)
        
        # Call video platform API
        video_url = call_video_platform_api(prompt)
        
        # Update task status
        storage.update_task(task_id, status=task_cfg.TASK_STATUS_FINISHED, result_url=video_url)
        
    except Exception as e:
        storage.update_task(task_id, status=task_cfg.TASK_STATUS_FAILED, error_message=str(e))

def perform_ocr(image_url: str) -> str:
    """Perform OCR recognition on image"""
    time.sleep(task_cfg.TASK_PROCESSING_TIME)
    
    if random.random() < task_cfg.OCR_FAILURE_RATE:
        raise Exception(error_cfg.ERROR_OCR_FAILED)
    
    return "Text content extracted from image"

def generate_prompt(text_content: str) -> str:
    """Generate prompt for video platform"""
    time.sleep(task_cfg.TASK_PROCESSING_TIME)
    
    if random.random() < task_cfg.PROMPT_FAILURE_RATE:
        raise Exception(error_cfg.ERROR_PROMPT_FAILED)
    
    return f"Animation prompt based on text: {text_content}"

def call_video_platform_api(prompt: str) -> str:
    """Call video platform API to generate animation"""
    time.sleep(task_cfg.TASK_PROCESSING_TIME)
    
    if random.random() < task_cfg.VIDEO_FAILURE_RATE:
        raise Exception(error_cfg.ERROR_VIDEO_FAILED)
    
    video_id = random.randint(1000, 9999)
    return task_cfg.VIDEO_URL_TEMPLATE.format(video_id=video_id) 