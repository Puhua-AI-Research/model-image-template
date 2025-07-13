import os, sys
import time
import numpy as np
import cv2

# 导出推理接口创建的统一实现
from package.backends import create_inference_api, get_inference_result

__all__ = [
    "Model"
]

# 统一的模型推理管理
class Model:
    def __init__(self):
        """模型管理初始化工作
        1. 读取环境变量: fastdeploy所需config文件自动从_model_path同目录读取(model.yaml)
        2. 其它相关工作
        """
        self._model_path = os.getenv("MODEL_PATH", "")
        self._params_path = os.getenv("PARAMS_PATH", "")
        self._model_name = os.getenv("MODEL_NAME", "")
        self._model_type = os.getenv("MODEL_TYPE", "")
        self._deploy_device = os.getenv("DEPLOY_DEVICE", "xpu")
        self._deploy_backend = os.getenv("DEPLOY_BACKEND", "fastdeploy")

    def load(self):
        """基于初始化结果构建推理后端，并加载模型
        1. 构建后端推理接口(需封装有包含前后处理，fastdeploy后端通过model.yaml自动加载，无需设计接口)
        2. 加载模型获取推理对象
        """
        _load_start_t = time.time()
        self.model = create_inference_api(
            model_name = self._model_name,
            model_type = self._model_type,
            model_path = self._model_path,
            params_path = self._params_path,
            deploy_device = self._deploy_device,
            deploy_backend = self._deploy_backend
        )
        print("Load Model and Create API Cost Time:", (time.time()-_load_start_t)*1000., "ms")

    def predict(self, data, **kwargs):
        """模型推理接口
        1. 输入图像文件数据作为输入数据，其余参数自定义传入
        2. 解析图像文件数据为opencv-mat数据，并传入推理接口
        3. 执行推理，并反馈推理结果——固定为json格式
            eg:
                {
                    "result": {
                        根据内容自行填充
                    }
                }
        """
        img = np.frombuffer(data, np.uint8) # 图像文件buffer转通用数组
        img_data = cv2.imdecode(img, cv2.IMREAD_COLOR) # 通用数组转图像数据
        result = get_inference_result(img_data, self.model, self._model_type, self._deploy_backend, **kwargs)
        return result
