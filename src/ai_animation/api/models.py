from typing import List, Optional
from pydantic import BaseModel
from ..config import settings

task_cfg = settings.task

class SubmitTaskRequest(BaseModel):
    """Request model for submitting animation generation tasks"""
    user_id: str
    input_type: str  # "text" or "image"
    input_content: str  # text content or image URL

class SubmitTaskResponse(BaseModel):
    """Response model for task submission"""
    task_id: str
    status: str

class QueryTaskStatusRequest(BaseModel):
    """Request model for querying task status"""
    task_id: str

class QueryTaskStatusResponse(BaseModel):
    """Response model for task status query"""
    task_id: str
    status: str
    result_url: Optional[str] = None
    error_message: Optional[str] = None

class ListTasksRequest(BaseModel):
    """Request model for listing user tasks"""
    user_id: str
    page: int = task_cfg.DEFAULT_PAGE
    page_size: int = task_cfg.DEFAULT_PAGE_SIZE

class TaskInfo(BaseModel):
    """Task information model"""
    task_id: str
    status: str
    created_at: str
    result_url: Optional[str] = None
    error_message: Optional[str] = None

class ListTasksResponse(BaseModel):
    """Response model for task list"""
    tasks: List[TaskInfo]
    total: int 