import fastdeploy as fd

# 导入模型推理结构注册函数
from package.fd.utils import register_inference_api


# 分类模型推理接口注册
def register_cls_inference_api(model_list):
    """由于FD对分类模型推理接口较为统一，大部分模型通用，因此可以直接注册
    """
    for model_name in model_list:
        register_inference_api("cls", model_name, fd.vision.classification.PaddleClasModel) # 若存在无法使用通用接口实现的，则需自行构建
    return model_list

register_cls_inference_api(
    ["mobilenetv1", "shufflenetv2"]
)
# 特别的模型可以手动注册
# register_inference_api(xxxx, xxxx, xxxx)




# 检测模型推理接口注册
register_inference_api("det", "yolov5", fd.vision.detection.PaddleYOLOv5)
register_inference_api("det", "yolov8", fd.vision.detection.PaddleYOLOv8)




# 分割模型推理接口注册
def register_seg_inference_api(model_list):
    """由于FD对分割模型推理接口较为统一，大部分模型通用，因此可以直接注册
    """
    for model_name in model_list:
        register_inference_api("seg", model_name, fd.vision.segmentation.PaddleSegModel) # 若存在无法使用通用接口实现的，则需自行构建
    return model_list

register_seg_inference_api(
    ["ppliteseg", "unet"]
)

print("register finished.")




