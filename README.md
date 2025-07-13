# 一、Demo介绍

- 构建可拓展多后端的模型管理(`deploymodel.py`)
- 接入`Fastdeploy`后端提供模型推理服务(已验证`XPU(R200)`)
  - 已验证模型: `mobilenetv1`(分类)、 `yolov5`(检测)、 `unet`(分割)

# 二、目录结构

> `Dockerfile`仅供参靠，部署服务时需自行核对环境变量是否正确以及服务文件是否拷贝！！！

```bash
- main.py # 服务启动代码，推理接口 `/predict` 接收: file, threshold, topk
- test_server.sh # 打包镜像前需自行测试目标接口是否可正常启动
- requirements.txt
- Dockerfile
- README.md
- package/ # 自定义推理库
	- __init__.py # 引出Model供外部调用
	- deploymodel.py # 实现外部接口Model
	- backends.py # 整合fd等目录下后端的推理接口
	- base_option.py # 通用推理配置项基类
	- model/ # 存放模型目录
		- model.nb # 存放序列化模型
		- model.yaml
	- fd/ # fastdeploy作为推理后端接口库——提供了基本的接口模板
		- __init__.py # 提供特定模型的推理接口
		- utils.py # 提供创建fastdeploy推理接口的创建函数，推理配置项的创建函数等
		- models.py # 注册各种模型的推理接口，具体结构可在该目录下自行实现后导入注册
- test_models/ # 测试模型文件目录
	- test_imgs/
		- cityscapes_demo.png
		- ILSVRC2012_val_00000010.jpeg
	- mobilenetv1/
		- model.nb
		- model.yaml
	- yolov5/
		- model.nb
		- model.yaml
	- unet/
		- model.nb
		- model.yaml
- docs/ # 相关文档
```

# 三、推理服务测试

- 通过`test_server.sh`启动服务测试:

```bash
# 参数说明
# model_path: 模型存放路径
# params_path: 权重路径 —— pdmodel模型时必须
# model_type: 模型类型 —— cls、det、seg
# model_name: 模型名 —— 用于搜索接口，需要与注册的模型推理接口(注册别名)一致
# deploy_device: 推理设备 —— 可用于运行时配置，避免运行在错误的设备
# deploy_backend: 后端类型 —— 目前仅支持fastdeploy，后期自行扩展后可改为其它后端

bash test_server.sh --model_path package/model/model.nb --params_path "" --model_type cls --model_name mobilenetv1 --deploy_device xpu --deploy_backend fastdeploy
```

- 运行日志位于同目录的`server.log`
- 健康检查接口: 

测试指令:

```bash
curl -X GET "http://localhost:8000/health"
```

运行结果:

```bash
{"status":"healthy"}
```

> 模型正常加载后即可访问该接口，否则无法访问——服务出发异常！！！

------

- 推理执行接口:

测试指令:

```bash
curl -X POST "http://localhost:8000/predict" \
-F "file=@/home/FD_server/test_models/test_imgs/ILSVRC2012_val_00000010.jpeg" \
-F "threshold=0.5"
```

运行结果:

```bash
"{\"label_ids\": [332], \"scores\": [0.5769524574279785]}"
```

------

测试指令:

```bash
curl -X POST "http://localhost:8000/predict" \
-F "file=@/home/FD_server/test_models/test_imgs/ILSVRC2012_val_00000010.jpeg" \
-F "topk=5"
```

运行结果:

```bash
"{\"label_ids\": [332, 153, 283, 229, 204], \"scores\": [0.5769524574279785, 0.21825027465820312, 0.08904066681861877, 0.03889011964201927, 0.020315099507570267]}"
```

------

# 四、相关文档

- [后端接口说明](docs/后端接口说明.md)
- [基于mobilenetv1的服务接口测试](docs/基于mobilenetv1的服务接口测试.md)
- [基于yolov5的服务接口测试](docs/基于yolov5的服务接口测试.md)
- [基于unet的服务接口测试](docs/基于unet的服务接口测试.md)
- [模型管理框架说明](docs/模型管理框架说明.md)
- [接入其它后端推理框架的说明](docs/接入其它后端推理框架的说明.md)
- [模型推理镜像制作与测试](docs/模型推理镜像制作与测试.md)
- [BPU推理服务测试](docs/BPU推理服务测试.md)
