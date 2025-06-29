# 服务健康检查功能说明

## 概述

AI动画生成平台提供了完整的健康检查功能，确保所有服务正常运行并及时发现潜在问题。

## 健康检查层级

### 1. Docker 容器健康检查

每个服务都配置了 Docker 健康检查：

#### Web 服务健康检查
```yaml
healthcheck:
  test: ["CMD-SHELL", "python -c \"import urllib.request; urllib.request.urlopen('http://localhost:8000/health')\""]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

#### Worker 服务健康检查
```yaml
healthcheck:
  test: ["CMD", "celery", "-A", "demo_ai.celery_app", "inspect", "ping"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 60s
```

#### Redis 健康检查
```yaml
healthcheck:
  test: ["CMD", "redis-cli", "ping"]
  interval: 10s
  timeout: 5s
  retries: 5
  start_period: 10s
```

#### MongoDB 健康检查
```yaml
healthcheck:
  test: ["CMD", "mongosh", "--username", "admin", "--password", "password", "--authenticationDatabase", "admin", "--eval", "db.adminCommand('ping')"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

### 2. API 健康检查端点

#### 健康检查接口
- **URL**: `GET /health`
- **响应**: 
```json
{
  "status": "healthy",
  "service": "AI Animation Platform"
}
```

#### 配置查看接口
- **URL**: `GET /config`
- **功能**: 显示当前配置（仅调试用）

### 3. 本地健康检查脚本

#### 脚本位置
- `local_health_check.sh` - 本地健康检查脚本

#### 检查项目
1. **容器状态检查**
   - 检查所有容器是否运行
   - 显示容器状态信息

2. **端口监听检查**
   - MongoDB 端口 (27017)
   - Web 服务端口 (8000)

3. **服务响应检查**
   - Web 服务 HTTP 响应
   - Redis 连接测试
   - MongoDB 连接测试
   - Celery Worker 状态检查

4. **健康状态检查**
   - 检查每个服务的健康状态
   - 显示健康/不健康/启动中状态

5. **错误日志检查**
   - 显示最近的错误日志

## 使用方法

### 启动时自动健康检查

```bash
./start.sh
```

启动脚本会：
1. 启动所有服务
2. 等待服务启动完成
3. 检查健康状态
4. 显示访问地址

### 手动健康检查

```bash
# 快速健康检查
./local_health_check.sh

# 查看容器状态
docker-compose ps

# 查看服务日志
docker-compose logs -f [service_name]
```

### 实时监控

```bash
# 启动实时监控
./monitor.sh
```

## 健康检查状态

### 状态类型

- **healthy**: 服务正常运行
- **unhealthy**: 服务异常
- **starting**: 服务启动中

### 检查命令

```bash
# 检查 Web 服务
curl -f http://localhost:8000/health

# 检查 Redis
docker-compose exec redis redis-cli ping

# 检查 MongoDB
docker-compose exec mongodb mongosh --username admin --password password --authenticationDatabase admin --eval "db.adminCommand('ping')"

# 检查 Celery Worker
docker-compose exec worker celery -A demo_ai.celery_app inspect ping
```

## 故障排除

### 常见问题

1. **服务启动失败**
   ```bash
   # 查看启动日志
   docker-compose logs [service_name]
   
   # 重启服务
   docker-compose restart [service_name]
   ```

2. **健康检查超时**
   ```bash
   # 增加启动等待时间
   # 修改 docker-compose.yml 中的 start_period
   ```

3. **依赖服务未就绪**
   ```bash
   # 检查依赖服务状态
   docker-compose ps
   
   # 按顺序启动服务
   docker-compose up -d redis mongodb
   docker-compose up -d web worker
   ```

### 调试技巧

1. **查看详细日志**
   ```bash
   docker-compose logs --tail=50 [service_name]
   ```

2. **进入容器调试**
   ```bash
   docker-compose exec [service_name] bash
   ```

3. **检查网络连接**
   ```bash
   docker-compose exec [service_name] ping [target_service]
   ```

## 监控集成

### 与外部监控系统集成

健康检查端点可以集成到：
- Prometheus
- Grafana
- Nagios
- Zabbix
- 自定义监控系统

### 告警配置

可以配置以下告警：
- 服务不可用
- 响应时间过长
- 错误率过高
- 资源使用率过高

## 最佳实践

1. **定期检查**: 建议每小时运行一次健康检查
2. **日志监控**: 持续监控错误日志
3. **性能监控**: 监控响应时间和资源使用
4. **自动恢复**: 配置自动重启失败的服务
5. **告警通知**: 设置及时的通知机制

## 配置优化

### 健康检查参数调优

```yaml
healthcheck:
  interval: 30s      # 检查间隔
  timeout: 10s       # 超时时间
  retries: 3         # 重试次数
  start_period: 40s  # 启动等待时间
```

### 根据服务特点调整

- **Web 服务**: 较短的检查间隔
- **数据库**: 较长的启动等待时间
- **Worker**: 适中的重试次数
- **缓存**: 快速的超时时间 