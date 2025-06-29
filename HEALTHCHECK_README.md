# 服务健康检查功能说明

## 概述

本项目已集成 Docker 健康检查功能，确保所有服务正常运行并自动检测问题。

## 健康检查配置

### 1. Redis 服务
- **检查命令**: `redis-cli ping`
- **检查间隔**: 10秒
- **超时时间**: 5秒
- **重试次数**: 5次
- **启动等待**: 10秒

### 2. MongoDB 服务
- **检查命令**: `mongosh --eval "db.adminCommand('ping')"`
- **检查间隔**: 30秒
- **超时时间**: 10秒
- **重试次数**: 3次
- **启动等待**: 40秒

### 3. Celery Worker 服务
- **检查命令**: `celery -A test.celery_app inspect ping`
- **检查间隔**: 30秒
- **超时时间**: 10秒
- **重试次数**: 3次
- **启动等待**: 60秒

### 4. Web 服务
- **检查命令**: `curl -f http://localhost:8000/health`
- **检查间隔**: 30秒
- **超时时间**: 10秒
- **重试次数**: 3次
- **启动等待**: 40秒

## 使用方法

### 启动服务
```bash
./start.sh
```
启动脚本会自动等待所有服务通过健康检查。

### 检查服务状态
```bash
# 快速健康检查
./health_check.sh

# 实时监控
./monitor.sh

# 查看容器状态
docker-compose ps

# 查看健康状态详情
docker inspect <container_name> | grep -A 10 "Health"
```

### 查看日志
```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f web
docker-compose logs -f worker
docker-compose logs -f redis
docker-compose logs -f mongodb
```

## 健康状态说明

- **healthy**: 服务正常运行
- **unhealthy**: 服务出现问题，需要检查
- **starting**: 服务正在启动中

## 故障排除

### 1. 服务启动失败
```bash
# 查看详细错误信息
docker-compose logs <service_name>

# 重启特定服务
docker-compose restart <service_name>

# 重新构建并启动
docker-compose down
docker-compose up --build -d
```

### 2. 健康检查失败
```bash
# 手动执行健康检查命令
docker-compose exec redis redis-cli ping
docker-compose exec mongodb mongosh --eval "db.adminCommand('ping')"
docker-compose exec web curl -f http://localhost:8000/health
docker-compose exec worker celery -A test.celery_app inspect ping
```

### 3. 依赖关系问题
服务启动顺序已通过 `depends_on` 和健康检查条件自动处理：
- Web 和 Worker 服务会等待 Redis 和 MongoDB 健康后才启动
- 所有服务都有适当的启动等待时间

## 监控建议

1. **定期检查**: 使用 `./health_check.sh` 定期检查服务状态
2. **实时监控**: 在生产环境中使用 `./monitor.sh` 进行实时监控
3. **日志分析**: 定期查看服务日志，及时发现潜在问题
4. **自动重启**: 考虑配置 Docker 的自动重启策略

## 性能优化

- 健康检查间隔可以根据实际需求调整
- 对于高负载环境，可以增加检查间隔时间
- 监控脚本的刷新频率可以通过修改 `sleep` 参数调整 