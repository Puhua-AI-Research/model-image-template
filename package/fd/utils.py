import os, sys
import json

import fastdeploy as fd

# 导入基本配置项，用于构建特定后端的配置项
from package.base_option import InferOption

__all__ = [
    "register_inference_api",
    "find_inference_api",
    "create_fd_inference_api",
    "create_fd_option",
    "process_fd_predict_result"
]

# 特定后端已注册接口采用字典接口进行缓存: {"cls": {"mobilenetv1": api1, "shullfulnetv2": api2}, "det": {}, "seg": {}}
FD_INFERENCE_APIS = {}
def register_inference_api(
        model_type: str,
        model_name: str,
        infer_api
    ):
    """注册推理接口
        1. model_type用于第一级注册分类
        2. model_name用于第二级注册分类
        3. infer_api为具体的接口实现(class)
    """
    # 导入全局变量
    global FD_INFERENCE_APIS
    if model_type not in FD_INFERENCE_APIS.keys():
        FD_INFERENCE_APIS[model_type] = {}
    if model_name not in FD_INFERENCE_APIS[model_type].keys(): # 运行时注册API
        FD_INFERENCE_APIS[model_type][model_name] = infer_api
    else:
        raise ValueError("({0} - register_inference_api) Model API({1}-{2}) has created, it should not registe repeatly.".format(
                    os.path.abspath(__file__), model_type, model_name))

def find_inference_api(
        model_type: str,
        model_name: str
    ):
    """查询已注册接口并返回接口
        1.model_type选定特定类型下的接口集合
        2.model_name选定指定模型的接口
    """
    if model_type in FD_INFERENCE_APIS.keys() and model_name in FD_INFERENCE_APIS[model_type].keys():
        return FD_INFERENCE_APIS[model_type][model_name]
    else:
        raise ValueError("({0} - find_inference_api) Model API({1}-{2}) don't find.".format(
                os.path.abspath(__file__), model_type, model_name))

def create_fd_inference_api(
        model_type: str,
        model_name: str
    ):
    """创建FD的推理接口——统一接口
    """
    _api = None
    _api = find_inference_api(model_type, model_name)
    return _api

def create_fd_option(
        model_path: str,
        params_path: str,
        config_path: str,
        deploy_device: str
    ):
    """构建FD后端推理的配置项——统一接口
    """
    _infer_option = InferOption()
    _infer_option.name = "fastdeploy"
    _infer_option.model_path = model_path
    _infer_option.params_path = params_path
    _infer_option.config_path = config_path
    _infer_option.deploy_device = deploy_device

    _runtime_option = fd.RuntimeOption() # FD特有运行时选项
    if deploy_device == "xpu":
        _runtime_option.use_lite_backend()
        _runtime_option.use_kunlunxin()
    elif deploy_device == "npu":
        _runtime_option.use_lite_backend()
        _runtime_option.use_ascend()
    elif deploy_device == "bpu":
        _runtime_option.use_sophgo()
    else:
        raise ValueError("({0} - create_fd_option) Deploy Device {1} is invalid, which only supports {2}.".format(
                os.path.abspath(__file__), deploy_device, ["xpu", "npu", "bpu"]))
    _infer_option.runtime_option = _runtime_option
    _infer_option.check_file_is_exists()
    return _infer_option

def process_fd_predict_result(
        result,
        model_type: str,
        **kwargs
    ):
    """解析FD后端推理结果为Json格式——统一接口
        1. 针对det检测模型结果进行阈值处理
        2. kwargs直接传入即可——默认处理threshold
    """
    if model_type == "det":
        _det_result = {
            "boxes": [],
            "scores": [],
            "label_ids": [],
            #"masks": [],
            #"contrain_masks": []
        }
        threshold = kwargs["threshold"]
        for idx, score in enumerate(result.scores):
            if score >= threshold:
                _det_result["boxes"].append(result.boxes[idx])
                _det_result["scores"].append(result.scores[idx])
                _det_result["label_ids"].append(result.label_ids[idx])
                # 不支持mask, 自行匹配测试后再开启该处理
                #_det_result["masks"].append(result.masks[idx])
                #_det_result["contain_masks"].append(result.contain_masks[idx])
        return json.dumps(_det_result)
    _result = fd.vision.utils.fd_result_to_json(result) # 获取Json格式结果
    return _result
