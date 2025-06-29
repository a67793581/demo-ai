from celery import Celery
import os

def get_redis_url():
    """Get Redis URL from settings"""
    # Get Redis URL directly, avoid importing settings
    redis_url = "redis://localhost:6379/0"
    if os.getenv('DOCKER_ENV') == 'true':
        redis_url = "redis://redis:6379/0"
    return redis_url

# Create Celery instance, directly specify broker
celery_app = Celery(
    "worker",
    broker=get_redis_url(),
    backend=get_redis_url(),
    include=['ai_animation.core.tasks']
)

# Configure Celery
celery_app.conf.update(
    broker_transport='redis',
    result_backend_transport='redis',
    broker_connection_retry_on_startup=True,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    # Explicitly specify not to use AMQP
    broker_transport_options={
        'visibility_timeout': 3600,
        'fanout_prefix': True,
        'fanout_patterns': True,
    },
    # Disable AMQP related configuration
    task_default_queue='default',
    task_default_exchange='default',
    task_default_routing_key='default',
)
