from typing import Dict, List, Tuple, Optional
from ..api.models import TaskInfo
from ..config import settings
import threading
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import sys

db_cfg = settings.db

class TaskStorage:
    """Task storage manager with MongoDB only - no fallback to file storage"""
    
    def __init__(self):
        self._lock = threading.Lock()
        
        # MongoDB connection objects
        self._mongo_client: Optional[MongoClient] = None
        self._mongo_db = None
        self._mongo_collection: Optional[Collection] = None
        self._init_mongodb()

    def _init_mongodb(self):
        """Initialize MongoDB connection and create indexes"""
        try:
            self._mongo_client = MongoClient(
                db_cfg.MONGO_URI, 
                serverSelectionTimeoutMS=db_cfg.CONNECTION_TIMEOUT
            )
            # Test connection
            self._mongo_client.admin.command('ping')
            
            self._mongo_db = self._mongo_client[db_cfg.MONGO_DATABASE]
            self._mongo_collection = self._mongo_db[db_cfg.MONGO_COLLECTION]
            
            # Create indexes for performance
            self._mongo_collection.create_index("task_id", unique=True)
            self._mongo_collection.create_index("user_id")
            
            print(f"✅ MongoDB connected successfully: {db_cfg.MONGO_URI}")
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"❌ MongoDB connection failed: {e}")
            print("Service will stop due to database connection failure.")
            sys.exit(1)
        except Exception as e:
            print(f"❌ MongoDB initialization failed: {e}")
            print("Service will stop due to database initialization failure.")
            sys.exit(1)

    def add_task(self, task: TaskInfo):
        """Add a new task to MongoDB storage"""
        if self._mongo_collection is None:
            raise Exception("MongoDB collection not initialized")
            
        with self._lock:
            try:
                task_dict = task.model_dump()
                self._mongo_collection.insert_one(task_dict)
            except Exception as e:
                print(f"❌ MongoDB save failed: {e}")
                raise Exception(f"Failed to save task to database: {e}")

    def get_task(self, task_id: str) -> Optional[TaskInfo]:
        """Retrieve a task by ID from MongoDB"""
        if self._mongo_collection is None:
            raise Exception("MongoDB collection not initialized")
            
        with self._lock:
            try:
                task_data = self._mongo_collection.find_one({"task_id": task_id})
                if task_data:
                    task_data.pop('_id', None)
                    return TaskInfo(**task_data)
                return None
            except Exception as e:
                print(f"❌ MongoDB query failed: {e}")
                raise Exception(f"Failed to retrieve task from database: {e}")

    def update_task(self, task_id: str, **kwargs):
        """Update task with new data in MongoDB"""
        if self._mongo_collection is None:
            raise Exception("MongoDB collection not initialized")
            
        with self._lock:
            try:
                update_data = {k: v for k, v in kwargs.items()}
                result = self._mongo_collection.update_one(
                    {"task_id": task_id},
                    {"$set": update_data}
                )
                if result.matched_count == 0:
                    raise Exception(f"Task not found: {task_id}")
            except Exception as e:
                print(f"❌ MongoDB update failed: {e}")
                raise Exception(f"Failed to update task in database: {e}")

    def list_tasks(self, user_id: str, page: int, page_size: int) -> Tuple[List[TaskInfo], int]:
        """List tasks for a user with pagination from MongoDB"""
        if self._mongo_collection is None:
            raise Exception("MongoDB collection not initialized")
            
        with self._lock:
            try:
                # Get total count
                total = self._mongo_collection.count_documents({"task_id": {"$regex": f"^{user_id}_"}})
                
                # Get paginated data
                cursor = self._mongo_collection.find(
                    {"task_id": {"$regex": f"^{user_id}_"}},
                    {"_id": 0}
                ).sort("created_at", -1).skip((page - 1) * page_size).limit(page_size)
                
                tasks = [TaskInfo(**task_data) for task_data in cursor]
                return tasks, total
            except Exception as e:
                print(f"❌ MongoDB query failed: {e}")
                raise Exception(f"Failed to list tasks from database: {e}")

    def close(self):
        """Close MongoDB connection"""
        if self._mongo_client:
            self._mongo_client.close()
            print("MongoDB connection closed.")

# Global storage instance
storage = TaskStorage() 