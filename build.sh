#!/bin/bash

# 构建依赖镜像
echo "构建依赖镜像..."
docker build -f Dockerfile.deps -t deps:latest .

# 检查依赖镜像构建是否成功
if [ $? -eq 0 ]; then
    echo "依赖镜像构建成功！"
    
    # 构建应用镜像
    echo "构建应用镜像..."
    docker build -f Dockerfile -t app:latest .
    
    if [ $? -eq 0 ]; then
        echo "应用镜像构建成功！"
        echo "所有镜像构建完成！"
    else
        echo "应用镜像构建失败！"
        exit 1
    fi
else
    echo "依赖镜像构建失败！"
    exit 1
fi 