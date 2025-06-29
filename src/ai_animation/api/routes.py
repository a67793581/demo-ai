from fastapi import APIRouter, HTTPException
from .models import (
    SubmitTaskRequest, SubmitTaskResponse,
    QueryTaskStatusRequest, QueryTaskStatusResponse,
    ListTasksRequest, ListTasksResponse, TaskInfo
)
from ..config import settings
from ..storage.storage import storage
from ..core.tasks import process_animation_task
import uuid
from datetime import datetime
from typing import Sequence

api_cfg = settings.api
task_cfg = settings.task

router = APIRouter(prefix=api_cfg.API_PREFIX, tags=list(api_cfg.API_TAGS))

@router.post("/submit-task", response_model=SubmitTaskResponse)
async def submit_task(request: SubmitTaskRequest):
    """Submit animation generation task"""
    task_id = f"{request.user_id}{api_cfg.TASK_ID_SEPARATOR}{uuid.uuid4().hex[:api_cfg.TASK_ID_SUFFIX_LENGTH]}"
    
    task_info = TaskInfo(
        task_id=task_id,
        status=task_cfg.TASK_STATUS_QUEUED,
        created_at=datetime.now().isoformat(),
        result_url=None,
        error_message=None
    )
    
    storage.add_task(task_info)
    process_animation_task.delay(task_id, request.user_id, request.input_type, request.input_content)
    
    return SubmitTaskResponse(task_id=task_id, status=task_cfg.TASK_STATUS_QUEUED)

@router.post("/query-status", response_model=QueryTaskStatusResponse)
async def query_task_status(request: QueryTaskStatusRequest):
    """Query task processing status"""
    task_info = storage.get_task(request.task_id)
    
    if not task_info:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return QueryTaskStatusResponse(
        task_id=task_info.task_id,
        status=task_info.status,
        result_url=task_info.result_url,
        error_message=task_info.error_message
    )

@router.post("/list-tasks", response_model=ListTasksResponse)
async def list_tasks(request: ListTasksRequest):
    """Get user task list with pagination"""
    tasks, total = storage.list_tasks(request.user_id, request.page, request.page_size)
    
    return ListTasksResponse(tasks=tasks, total=total) 