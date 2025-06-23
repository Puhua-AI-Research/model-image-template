# YOLO 图像推理服务

这是一个基于 FastAPI 的 YOLO 图像推理服务，支持 Docker 容器化部署。

## 功能特性

- ✅ **FastAPI Web 框架** - 高性能异步 API 服务
- ✅ **YOLO 模型推理** - 专门针对 YOLOv8 目标检测
- ✅ **图像上传处理** - 支持图像文件上传和推理
- ✅ **置信度阈值** - 可调节的检测置信度阈值
- ✅ **健康检查** - 服务状态监控
- ✅ **Docker 支持** - 完整的容器化部署方案
- ✅ **API 文档** - 自动生成的 OpenAPI 文档

## 快速开始

### 1. 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 确保有 package 模块和 yolov8n.pt 模型文件

# 运行服务
python main.py
```

### 2. Docker 部署

```bash
# 构建镜像
docker build -t yolo-inference-service .

# 运行容器
docker run -p 8000:8000 yolo-inference-service
```

### 3. 访问服务

- **API 文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health

## API 接口

### 健康检查

```bash
curl http://localhost:8000/health
```

### 图像推理

```bash
# 上传图片进行目标检测
curl -X POST http://localhost:8000/predict \
  -F "file=@your_image.jpg" \
  -F "threshold=0.5"
```

**参数说明：**
- `file`: 图片文件（必需）
- `threshold`: 置信度阈值，范围 0.0-1.0（默认 0.5）

## 代码结构

```python
# main.py 主要组件

# 1. 模型初始化
from package import Model
model = Model(model_name="yolov8n", model_path="yolov8n.pt")
model.load()

# 2. 推理接口
@app.post("/predict")
async def predict(request: InferenceRequest):
    image = await request.file.read()
    result = model.predict(image)
    return result
```

## 环境变量配置

- `HOST`: 服务绑定地址 (默认: 0.0.0.0)
- `PORT`: 服务端口 (默认: 8000)
- `WORKERS`: 工作进程数 (默认: 1)

## 目录结构

```
.
├── main.py                 # 主应用文件
├── requirements.txt        # Python 依赖
├── Dockerfile             # Docker 镜像构建文件
├── .dockerignore          # Docker 忽略文件
├── README.md              # 说明文档
├── package/               # 模型包目录
│   └── __init__.py        # Model 类实现
├── yolov8n.pt            # YOLO 模型文件
└── logs/                  # 日志文件目录
```

## 自定义扩展

### 1. 更换模型

修改模型初始化部分：

```python
# 使用不同的 YOLO 模型
model = Model(model_name="yolov8s", model_path="yolov8s.pt")
# 或者
model = Model(model_name="yolov8m", model_path="yolov8m.pt")
```

### 2. 添加预处理

在 `predict` 函数中添加图像预处理：

```python
@app.post("/predict")
async def predict(request: InferenceRequest):
    image = await request.file.read()
    
    # 添加图像预处理
    # processed_image = preprocess(image)
    
    result = model.predict(image, threshold=request.threshold)
    return result
```

### 3. 扩展返回结果

根据需要格式化推理结果：

```python
result = model.predict(image)
return {
    "detections": result,
    "timestamp": datetime.now().isoformat(),
    "model_name": "yolov8n",
    "threshold": request.threshold
}
```

## 部署建议

### 开发环境

```bash
python main.py
```

### 生产环境

```bash
# 使用 uvicorn 启动
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# 或者使用 Docker
docker run -d -p 8000:8000 --name yolo-service yolo-inference-service
```

### 性能优化

1. **GPU 支持**: 在 Dockerfile 中添加 CUDA 支持
2. **模型优化**: 使用 TensorRT 或 ONNX 优化模型
3. **并发处理**: 根据硬件配置调整 workers 数量

## 依赖要求

- Python 3.11+
- FastAPI
- uvicorn
- package (自定义模型包)
- yolov8n.pt (YOLO 模型文件)

## 常见问题

**Q: 如何添加新的 YOLO 模型？**
A: 将模型文件放入项目目录，并修改 `Model` 初始化参数。

**Q: 支持哪些图像格式？**
A: 支持常见的图像格式：JPG, PNG, BMP, TIFF 等。

**Q: 如何调整检测精度？**
A: 通过 `threshold` 参数调整置信度阈值，值越高精度越高但召回率越低。

## 许可证

MIT License 