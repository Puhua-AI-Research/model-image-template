# 使用官方 Python 3.11 镜像作为基础镜像 -- 需修改为目标推理镜像
FROM python:3.11-slim


# 安装系统依赖(按需下载)
#RUN apt-get update && apt-get install -y \
#    gcc \
#    g++ \
#    curl \
#    && rm -rf /var/lib/apt/lists/*

# todo: 安装cuda 或者 其他硬件的软件栈

# 设置工作目录
WORKDIR /app

# 拷贝服务目录到WORKDIR(当前目录下已包含模型文件，若不包含请自行拷贝)
COPY . .

# 安装 Python 依赖(如果需要自行取消注释)
#RUN pip install --upgrade pip && \
#    pip install -r /app/requirements.txt

# 暴露端口(与后续启动端口保持一致)
EXPOSE 8000

# 配置环境变量(需根据实际服务自行修改)
ENV MODEL_PATH=/app/package/model/model.nb \
    PARAMS_PATH="" \
    MODEL_TYPE=cls \
    MODEL_NAME=mobilenetv1 \
    DEPLOY_DEVICE=xpu \
    DEPLOY_BACKEND=fastdeploy

# 使用 uvicorn 直接启动（更适合生产环境）
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"] 
