# 使用官方 Python 3.11 镜像作为基础镜像
FROM python:3.11-slim


# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# todo: 安装cuda 或者 其他硬件的软件栈

# 复制依赖文件
COPY requirements.txt /tmp/requirements.txt

# 设置工作目录
WORKDIR /app

# 安装 Python 依赖
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8000


# 可选：使用 uvicorn 直接启动（更适合生产环境）
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"] 