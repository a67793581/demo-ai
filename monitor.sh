#!/bin/bash

echo "=== 服务监控模式 ==="
echo "按 Ctrl+C 退出监控"
echo ""

# 设置颜色
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

while true; do
    # 清屏
    clear
    
    echo -e "${GREEN}=== AI 动画服务监控 ===${NC}"
    echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    
    # 显示容器状态
    echo "容器状态:"
    docker-compose ps
    
    echo ""
    echo "健康状态详情:"
    
    # 检查每个服务的健康状态
    services=("redis" "mongodb" "worker" "web")
    all_healthy=true
    
    for service in "${services[@]}"; do
        health_status=$(docker-compose ps $service | grep -o "healthy\|unhealthy\|starting" | head -1)
        if [ "$health_status" = "healthy" ]; then
            echo -e "  ${GREEN}✅ $service: 健康${NC}"
        elif [ "$health_status" = "starting" ]; then
            echo -e "  ${YELLOW}⏳ $service: 启动中${NC}"
            all_healthy=false
        else
            echo -e "  ${RED}❌ $service: 不健康${NC}"
            all_healthy=false
        fi
    done
    
    echo ""
    if [ "$all_healthy" = true ]; then
        echo -e "${GREEN}🎉 所有服务运行正常！${NC}"
    else
        echo -e "${YELLOW}⚠️  部分服务需要关注${NC}"
    fi
    
    echo ""
    echo "最近日志 (最后 5 行):"
    docker-compose logs --tail=5 2>/dev/null || echo "无法获取日志"
    
    echo ""
    echo "按 Ctrl+C 退出监控"
    
    # 等待 5 秒后刷新
    sleep 5
done 