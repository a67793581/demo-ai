#!/bin/bash

echo "启动 AI 动画服务..."
docker-compose down

docker-compose up -d

echo "等待服务启动..."
while true; do
    running_count=$(docker-compose ps | grep -c "Up")
    total_count=$(docker-compose ps | grep -c "test-")
    if [ "$running_count" -eq "$total_count" ] && [ "$total_count" -gt 0 ]; then
        if curl -s -f http://localhost:8000/health >/dev/null 2>&1; then
            echo "所有服务已启动并健康！"
            break
        fi
    fi
    sleep 3
done

echo "Web 服务地址: http://localhost:8000" 