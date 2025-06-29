#!/bin/bash

echo "=== 本地服务健康检查 ==="

# 设置颜色
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 检查容器状态
echo "1. 检查容器状态:"
docker-compose ps

echo -e "\n2. 检查端口监听:"

# 检查 MongoDB 端口
if netstat -an 2>/dev/null | grep -q "\.27017.*LISTEN" || lsof -i :27017 >/dev/null 2>&1; then
    echo -e "${GREEN}✅ MongoDB 端口 (27017) 正常监听${NC}"
else
    echo -e "${RED}❌ MongoDB 端口 (27017) 未监听${NC}"
fi

# 检查 Web 端口
if netstat -an 2>/dev/null | grep -q "\.8000.*LISTEN" || lsof -i :8000 >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Web 端口 (8000) 正常监听${NC}"
else
    echo -e "${RED}❌ Web 端口 (8000) 未监听${NC}"
fi

echo -e "\n3. 检查服务响应:"

# 检查 Web 服务响应
if curl -s -f http://localhost:8000/health >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Web 服务响应正常${NC}"
else
    echo -e "${RED}❌ Web 服务无响应${NC}"
fi

# 检查 Redis 连接
if docker-compose exec -T redis redis-cli ping >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Redis 服务正常${NC}"
else
    echo -e "${RED}❌ Redis 服务异常${NC}"
fi

# 检查 MongoDB 连接
if docker-compose exec -T mongodb mongosh --eval "db.adminCommand('ping')" >/dev/null 2>&1; then
    echo -e "${GREEN}✅ MongoDB 服务正常${NC}"
else
    echo -e "${RED}❌ MongoDB 服务异常${NC}"
fi

# 检查 Celery Worker
if docker-compose exec -T worker celery -A test.celery_app inspect ping >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Celery Worker 正常${NC}"
else
    echo -e "${RED}❌ Celery Worker 异常${NC}"
fi

echo -e "\n4. 检查服务健康状态:"
services=("redis" "mongodb" "worker" "web")

for service in "${services[@]}"; do
    health_status=$(docker-compose ps $service | grep -o "healthy\|unhealthy\|starting" | head -1)
    if [ "$health_status" = "healthy" ]; then
        echo -e "  ${GREEN}✅ $service: 健康${NC}"
    elif [ "$health_status" = "starting" ]; then
        echo -e "  ${YELLOW}⏳ $service: 启动中${NC}"
    else
        echo -e "  ${RED}❌ $service: 不健康${NC}"
    fi
done

echo -e "\n5. 最近错误日志:"
docker-compose logs --tail=5 2>/dev/null | grep -i error || echo "没有发现错误日志"

echo -e "\n=== 检查完成 ===" 