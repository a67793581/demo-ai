from celery import Celery
import os

def get_redis_url():
    """Get Redis URL from settings"""
    # 直接获取Redis URL，避免导入settings
    redis_url = "redis://localhost:6379/0"
    if os.getenv('DOCKER_ENV') == 'true':
        redis_url = "redis://redis:6379/0"
    return redis_url

# 创建 Celery 实例，直接指定broker
celery_app = Celery(
    "worker",
    broker=get_redis_url(),
    backend=get_redis_url(),
    include=['ai_animation.core.tasks']
)

# 配置 Celery
celery_app.conf.update(
    broker_transport='redis',
    result_backend_transport='redis',
    broker_connection_retry_on_startup=True,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    # 明确指定不使用AMQP
    broker_transport_options={
        'visibility_timeout': 3600,
        'fanout_prefix': True,
        'fanout_patterns': True,
    },
    # 禁用AMQP相关配置
    task_default_queue='default',
    task_default_exchange='default',
    task_default_routing_key='default',
)
