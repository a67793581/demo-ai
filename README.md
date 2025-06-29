# AI 动画生成平台

一个基于 FastAPI + Celery + Redis + MongoDB 的 AI 驱动动画生成平台，支持文字和图片输入，通过 OCR 识别、Prompt 生成和第三方视频平台 API 生成教学动画。

## 🚀 项目特性

- **异步任务处理**: 基于 Celery + Redis 的队列系统，支持高并发任务处理
- **多输入支持**: 支持文字和图片输入，自动 OCR 识别
- **模块化架构**: 清晰的业务逻辑与存储层分离
- **容器化部署**: 完整的 Docker 支持，一键部署
- **健康检查**: 内置服务健康监控和自动故障检测
- **MongoDB 认证**: 安全的数据库连接和认证机制
- **实时监控**: 提供实时服务状态监控脚本

## 📋 系统架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   前端界面      │    │   FastAPI       │    │   Celery        │
│   (Web UI)      │◄──►│   (API Server)  │◄──►│   (Worker)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │     Redis       │    │    MongoDB      │
                       │   (Message      │    │   (Task Storage)│
                       │    Queue)       │    │                 │
                       └─────────────────┘    └─────────────────┘
```

## 🛠️ 技术栈

- **后端框架**: FastAPI (Python 3.13)
- **任务队列**: Celery + Redis
- **数据库**: MongoDB 7.0 (带认证)
- **容器化**: Docker + Docker Compose
- **依赖管理**: Poetry
- **健康检查**: Docker Health Checks

## 📁 项目结构

```
demo-ai/
├── src/
│   ├── ai_animation/
│   │   ├── api/                 # API 层
│   │   │   ├── models.py        # 数据模型
│   │   │   └── routes.py        # API 路由
│   │   ├── config/              # 配置层
│   │   │   ├── api.py           # API 配置
│   │   │   ├── app.py           # 应用配置
│   │   │   ├── base.py          # 基础配置
│   │   │   ├── db.py            # 数据库配置
│   │   │   ├── error.py         # 错误配置
│   │   │   ├── redis.py         # Redis 配置
│   │   │   └── task.py          # 任务配置
│   │   ├── core/                # 核心业务逻辑
│   │   │   └── tasks.py         # Celery 任务
│   │   ├── storage/             # 存储层 (独立模块)
│   │   │   └── storage.py       # MongoDB 存储实现
│   │   └── utils/               # 工具模块
│   └── demo_ai/
│       ├── celery_app.py        # Celery 应用配置
│       ├── main.py              # FastAPI 主应用
│       ├── static/              # 静态文件
│       └── templates/           # 模板文件
├── docker-compose.yml           # Docker Compose 配置
├── Dockerfile                   # 应用镜像构建
├── Dockerfile.deps              # 依赖镜像构建
├── pyproject.toml               # Poetry 配置
├── start.sh                     # 启动脚本
├── stop.sh                      # 停止脚本
├── build.sh                     # 构建脚本
├── local_health_check.sh        # 本地健康检查
├── monitor.sh                   # 实时监控脚本
└── README.md                    # 项目文档
```

## 🚀 快速开始

### 环境要求

- Docker & Docker Compose
- Python 3.13+ (本地开发)
- Poetry (本地开发)

### 1. 克隆项目

```bash
git clone https://github.com/a67793581/demo-ai.git
cd demo-ai
```

### 2. 构建镜像

```bash
./build.sh
```

### 3. 启动服务

```bash
./start.sh
```

启动脚本会自动：
- 构建并启动所有 Docker 容器
- 等待所有服务通过健康检查
- 显示服务状态和访问地址

### 4. 访问服务

- **Web 界面**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health

## 🔧 开发环境

### 本地开发设置

1. **安装依赖**
```bash
poetry install
```

2. **启动依赖服务**
```bash
docker-compose up -d redis mongodb
```

3. **启动应用服务**
```bash
# 启动 FastAPI 服务
PYTHONPATH=src poetry run uvicorn demo_ai.main:app --host 0.0.0.0 --port 8000 --reload

# 启动 Celery Worker (新终端)
PYTHONPATH=src poetry run celery -A demo_ai.celery_app worker --loglevel=info
```

## 📊 服务监控

### 健康检查

```bash
# 快速健康检查
./local_health_check.sh

# 实时监控
./monitor.sh
```

### 查看服务状态

```bash
# 查看容器状态
docker-compose ps

# 查看服务日志
docker-compose logs -f [service_name]
```

## 🔌 API 接口

### 提交任务

```bash
curl -X POST "http://localhost:8000/ai-animation/submit-task" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "input_type": "text",
    "input_content": "生成一个关于太阳系的动画"
  }'
```

### 查询任务状态

```bash
curl -X POST "http://localhost:8000/ai-animation/query-status" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "user123_abc12345"
  }'
```

### 获取任务列表

```bash
curl -X POST "http://localhost:8000/ai-animation/list-tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "page": 1,
    "page_size": 10
  }'
```

## ⚙️ 配置说明

### 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `DOCKER_ENV` | `false` | 是否在 Docker 环境中运行 |
| `MONGO_USERNAME` | `admin` | MongoDB 用户名 |
| `MONGO_PASSWORD` | `password` | MongoDB 密码 |

### 服务配置

- **Redis**: 端口 6379，无认证
- **MongoDB**: 端口 27017，用户名/密码认证
- **Web 服务**: 端口 8000
- **Celery Worker**: 自动连接到 Redis

## 🔒 安全说明

- MongoDB 使用用户名/密码认证
- 所有数据库操作都有异常处理和日志记录
- 服务间通信使用内部网络
- 健康检查确保服务可用性

## 🐛 故障排除

### 常见问题

1. **MongoDB 连接失败**
   ```bash
   # 检查 MongoDB 容器状态
   docker-compose ps mongodb
   
   # 查看 MongoDB 日志
   docker-compose logs mongodb
   ```

2. **Celery Worker 无法启动**
   ```bash
   # 检查 Redis 连接
   docker-compose exec redis redis-cli ping
   
   # 查看 Worker 日志
   docker-compose logs worker
   ```

3. **服务健康检查失败**
   ```bash
   # 运行健康检查脚本
   ./local_health_check.sh
   ```

### 重启服务

```bash
# 重启特定服务
docker-compose restart [service_name]

# 重启所有服务
docker-compose down
docker-compose up -d
```

## 📈 性能优化

- 所有任务处理时间统一设置为 3 秒（便于测试）
- MongoDB 已创建 task_id 和 user_id 索引
- Redis 连接池优化
- Celery Worker 并发数可配置

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

- 项目维护者: Carlo (jiangbingjie1218@gmail.com)
- 项目链接: [https://github.com/a67793581/demo-ai.git](https://github.com/a67793581/demo-ai.git)

---

**注意**: 这是一个演示项目，生产环境部署前请根据实际需求调整配置和安全设置。