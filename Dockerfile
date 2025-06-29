FROM deps:latest

WORKDIR /app

# 复制项目文件
COPY pyproject.toml poetry.lock README.md ./
# 复制应用代码（提前）
COPY src/ ./src/

# 安装依赖（此时包已存在）
RUN poetry install

# 设置默认命令
CMD ["uvicorn", "test.main:app", "--host", "0.0.0.0", "--port", "8000"]
