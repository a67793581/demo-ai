#!/bin/bash

echo "检查环境配置文件..."

# 检查 .env 文件是否存在
if [ ! -f .env ]; then
    echo ".env 文件不存在，检查 .env.example 文件..."
    if [ -f .env.example ]; then
        echo "复制 .env.example 为 .env..."
        cp .env.example .env
        echo ".env 文件已创建"
    else
        echo "警告: .env.example 文件也不存在，将使用默认配置"
        # 创建基本的 .env 文件
        cat > .env << EOF
# AI 动画生成平台环境变量配置
DOCKER_ENV=false
MONGO_USERNAME=admin
MONGO_PASSWORD=password
MONGO_HOST=mongodb
MONGO_PORT=27017
MONGO_DATABASE=ai_animation
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
API_HOST=0.0.0.0
API_PORT=8000
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
LOG_LEVEL=INFO
EOF
        echo "已创建默认 .env 文件"
    fi
else
    echo ".env 文件已存在"
fi

echo "启动 AI 动画服务..."
docker-compose down

docker-compose up -d

echo "等待服务启动..."
while true; do
    # 获取当前目录名作为项目名
    PROJECT_NAME=$(basename $(pwd))
    running_count=$(docker-compose ps | grep -c "Up")
    total_count=$(docker-compose ps | grep -c "${PROJECT_NAME}-")
    if [ "$running_count" -eq "$total_count" ] && [ "$total_count" -gt 0 ]; then
        if curl -s -f http://localhost:8000/health >/dev/null 2>&1; then
            echo "所有服务已启动并健康！"
            break
        fi
    fi
    sleep 3
done

echo "Web 服务地址: http://localhost:8000" 