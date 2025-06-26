# 引出后端的推理接口创建函数、配置项创建函数和推理结果处理函数供外部调用
from package.fd.utils import create_fd_inference_api, create_fd_option, process_fd_predict_result

# 导入后端的models完成后端推理接口的注册
import package.fd.models
