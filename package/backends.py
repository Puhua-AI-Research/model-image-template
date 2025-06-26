import os, sys

# 导入fastdeploy后端的推理接口创建函数、配置项创建函数以及推理结果处理函数
from package.fd import create_fd_inference_api, create_fd_option, process_fd_predict_result
# 其余后端类似导入接口
# from package.xxxx import create_xx_inference_api, create_xx_option, process_xx_predict_result

__all__ = [
    "valid_backend_list",
    "create_inference_api",
    "get_inference_result"
]

# 已实现的后端: 添加新后端后需将其名字添入
valid_backend_list = [
    "fastdeploy"
]


def _create_backend(
        model_name: str,
        model_type: str,
        deploy_backend: str
    ):
    """创建后端接口
        1. deploy_backend选择合适的后端创建接口
        2. 通过model_type和model_name创建目标推理接口
    """
    _api = None
    if deploy_backend == "fastdeploy": # 创建fastdeploy推理接口
        _api = create_fd_inference_api(
            model_type, model_name
        )
    #elif deploy_backend == "xxxx":
    #    pass
    else: # 不满足运行要求直接抛出异常，避免服务错误启动
        raise ValueError("({0} - _create_backend) Backend {1} is not invalid, which only supports {2}.".format(
            os.path.abspath(__file__), deploy_backend, valid_backend_list))
    return _api

def _create_option(
        model_path: str,
        params_path: str,
        deploy_device: str,
        deploy_backend: str,
    ):
    """创建后端接口所需的配置项
        1. model_path和params_path记录到option，以备接口实例时入口参数所需
        2. deploy_device用于特定的后端配置
        3. deploy_backend用于选择合适的后端配置项创建接口
    """
    _option = None
    if deploy_backend == "fastdeploy":
        # 从model_path自动提取config文件
        config_path = os.path.join(os.path.dirname(os.path.abspath(model_path)), "model.yaml")
        _option = create_fd_option(
            model_path, params_path, config_path, deploy_device
        )
    #elif deploy_backend == "xxxx":
    #    pass
    else: # 不满足运行要求直接抛出异常，避免服务错误启动
        raise ValueError("({0} - _create_option): Backend {1} is not invalid, which only supports {2}.".format(
                os.path.abspath(__file__), deploy_backend, valid_backend_list))
    return _option

def _create_model(
        infer_api,
        infer_option
    ):
    """基于api和option创建模型用于推理
        1. infer_api对应目标推理接口
        2. infer_option对应目标推理的配置项
    """
    _model = None
    if infer_option.name == "fastdeploy":
        _model = infer_api(
            infer_option.model_path,
            infer_option.params_path,
            infer_option.config_path,
            runtime_option = infer_option.runtime_option
        ) # 基于配置项自主构建有效的推理接口实例
    #elif deploy_backend == "xxxx":
    #    pass
    else: # 不满足运行要求直接抛出异常，避免服务错误启动
        raise ValueError("({0} - _create_model): Backend {1} is not invalid, which only supports {2}.".format(
                os.path.abspath(__file__), deploy_backend, valid_backend_list))
    return _model


def create_inference_api(
        model_name: str,
        model_type: str,
        model_path: str,
        params_path: str,
        deploy_device: str,
        deploy_backend: str,
    ):
    """创建推理接口 —— 统一推理接口
    1. 基于deploy_backend选定后端
    2. 基于model_name以及model_type选定后端已注册的推理接口
    3. 其余参数为配置项信息
    """
    _api = None
    _api = _create_backend(model_name, model_type, deploy_backend) # 获取指定后端的推理接口
    _option = None
    _option = _create_option(model_path, params_path, deploy_device, deploy_backend) # 获取指定后端推理的配置项
    _model = None
    _model = _create_model(_api, _option) # 实例化推理接口
    return _model

def get_inference_result(
        img,
        model,
        model_type: str,
        deploy_backend: str,
        **kwargs
    ):
    """不同后端对不同类型模型的输出结果处理方式不同，因此封装推理结果为Json格式
        1. img为opencv图像数据
        2. model对应实例化推理接口: 需总是包含predict函数，且至少包含输入图像数据的入口参数，其余参数为默认参数值
        3. model_type用于配置推理处理: cls允许传入topk，det允许传入threshold
        4. deploy_backend用于选择对应后端的推理结果处理接口
        eg:
           _result: {
                "result": {
                    Json形式的结果
                }
           }
    """
    _result = None
    predict_result = model.predict(img, 1 if "topk" not in kwargs.keys() else kwargs["topk"]) if model_type == "cls" else model.predict(img)
    if deploy_backend == "fastdeploy":
        _result = process_fd_predict_result(predict_result, model_type, **kwargs) # 通常只需要对det的检测结果作threshold过滤即可
    #elif deploy_backend == "xxxx":
    #    pass
    else: # 不满足运行要求直接抛出异常，避免服务错误启动
        raise ValueError("({0} - get_inference_result): Backend {1} is not invalid, which only supports {2}.".format(
                os.path.abspath(__file__), deploy_backend, valid_backend_list))
    return _result
