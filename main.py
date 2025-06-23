#!/usr/bin/env python3
"""
模型推理服务模版
Model Inference Service Template
"""

import os
import json
import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
import traceback

import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from package import Model

model = Model(model_name="yolov8n", model_path="yolov8n.pt")
model.load()

# 创建FastAPI应用
app = FastAPI(
    title="模型推理服务",
    description="Model Inference Service Template",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


class InferenceRequest(BaseModel):
    """推理请求模型"""
    file: UploadFile = File(..., description="上传图片文件")
    threshold: float = Field(default=0.5, ge=0.0, le=1.0, description="置信度阈值")


@app.post("/predict")
async def predict(request: InferenceRequest):
    """执行推理"""
    # 读取图片
    image = await request.file.read()
    # 调用模型推理
    result = model.predict(image)
    return result
    

if __name__ == "__main__":
    # 获取配置
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    workers = int(os.getenv("WORKERS", 1))
    
    # 运行服务
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        workers=workers,
        reload=False,
        access_log=True
    )
