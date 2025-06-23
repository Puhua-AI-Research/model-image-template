# 模型管理器


class Model:
    def __init__(self, model_name: str, model_path: str):
        self.model_name = model_name
        self.model_path = model_path

    def load(self):
        pass

    def predict(self, **kwargs):
        pass
