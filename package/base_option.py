import os, sys

__all__ = [
    "InferOption"
]

class InferOption:
    """推理配置项：所有后端均可引用，用于构建特定后端推理引擎的配置
        eg:
            对于fastdeploy:
                fd_option = InferOoption()
                fd_option.name = "fastdeploy"
                fd_option.model_path = "xxxxx"
                ....
    """
    def __init__(self):
        self.name = "" # 由后端创建option时指定
        self.model_path = ""
        self.params_path = ""
        self.config_path = "" # fastdpeloy时务必配置
        self.deploy_device = ""
        self.runtime_option = None # 后端运行时选项，fastdeploy务必配置

    def check_file_is_exists(self):
        """检查必要的文件是否存在——当前以Fastdeploy为例设置文件检查
        """
        if not os.path.exists(self.model_path) or self.model_path == "":
            raise ValueError("model_path is not exists or it is empty.")
        if self.model_path.split(".")[-1] == "pdmodel":
            if not os.path.exists(self.params_path) or self.params_path == "":
                raise ValueError("params_path is not exists or it is empty.")
        if self.name == "fastdeploy":
            if not os.path.exists(self.config_path) or self.config_path == "":
                raise ValueError("config_path is not exists or it is empty.")
 

