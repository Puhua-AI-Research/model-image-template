# 一、测试指令

> 注意将`model_path`设置为`xpu`序列化`nb`模型的路径，并在同一级目录存放`model.yaml`的推理配置文件。

```bash
# 参数说明
# model_path: 模型存放路径
# params_path: 权重路径 —— pdmodel模型时必须
# model_type: 模型类型 —— cls、det、seg
# model_name: 模型名 —— 用于搜索接口，需要与注册的模型推理接口(注册别名)一致
# deploy_device: 推理设备 —— 可用于运行时配置，避免运行在错误的设备
# deploy_backend: 后端类型 —— 目前仅支持fastdeploy，后期自行扩展后可改为其它后端

bash test_server.sh --model_path package/model/model.nb --params_path "" --model_type det --model_name yolov5 --deploy_device xpu --deploy_backend fastdeploy
```

------

# 二、服务状态/关闭指令

查看运行状态:

```bash
ps aux | grep uvicorn
#### 日志如下: ####
root        7057 68.7  0.0 3103616 155392 pts/0  Sl   19:10   0:06 /opt/py310/bin/python3.10 /opt/py310/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1
root        7128  0.0  0.0 214464  1216 pts/0    S+   19:10   0:00 grep --color=always uvicorn
```

查看运行日志:

```bash
cat server.log
#### 日志如下: ####
XPURT /opt/py310/lib/python3.10/site-packages/fastdeploy/libs/third_libs/paddlelite/lib/../third_party/xpu/xdnn/so/libxpurt.so.1 loaded
[INFO] fastdeploy/vision/common/processors/transform.cc(93)::FuseNormalizeHWC2CHW       Normalize and HWC2CHW are fused to NormalizeAndPermute  in preprocessing pipeline.
[INFO] fastdeploy/vision/common/processors/transform.cc(159)::FuseNormalizeColorConvert BGR2RGB and NormalizeAndPermute are fused to NormalizeAndPermute with swap_rb=1
[INFO] fastdeploy/runtime/runtime.cc(328)::CreateLiteBackend    Runtime initialized with Backend::PDLITE in Device::KUNLUNXIN.
INFO:     Started server process [7057]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

终止服务:

```bash
pkill -f "uvicorn main:app"
```

------



# 三、服务接口测试

## 3.1 health测试

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

## 3.2 predict测试(基于nb模型文件)

测试指令1:

```bash
curl -X POST "http://localhost:8000/predict" \
-F "file=@/home/FD_server/test_models/test_imgs/ILSVRC2012_val_00000010.jpeg" \
-F "threshold=0.1" \
-F "topk=1"
```

运行结果1:

```bash
"{\"boxes\": [[4.613542556762695, 8.172739028930664, 491.4633483886719, 362.0327453613281], [9.589195251464844, 0.5111575126647949, 503.5101013183594, 223.6992950439453],...,], \"scores\": [...], \"label_ids\": [...]}"
```

------

测试指令2:

```bash
curl -X POST "http://localhost:8000/predict" \
-F "file=@/home/FD_server/test_models/test_imgs/ILSVRC2012_val_00000010.jpeg" \
-F "threshold=0.5"
```

运行结果2:

```bash
"{\"boxes\": [], \"scores\": [], \"label_ids\": []}"
```

------

测试指令3:

```bash
curl -X POST "http://localhost:8000/predict" \
-F "file=@/home/FD_server/test_models/test_imgs/ILSVRC2012_val_00000010.jpeg" \
-F "topk=5"
```

运行结果3:

```bash
"{\"boxes\": [], \"scores\": [], \"label_ids\": [], \"masks\": [], \"contrain_masks\": []}"
```

------

# 四、完整服务的测试运行日志

```bash
XPURT /opt/py310/lib/python3.10/site-packages/fastdeploy/libs/third_libs/paddlelite/lib/../third_party/xpu/xdnn/so/libxpurt.so.1 loaded
[INFO] fastdeploy/vision/common/processors/transform.cc(45)::FuseNormalizeCast  Normalize and Cast are fused to Normalize in preprocessing pipeline.
[INFO] fastdeploy/vision/common/processors/transform.cc(93)::FuseNormalizeHWC2CHW       Normalize and HWC2CHW are fused to NormalizeAndPermute  in preprocessing pipeline.
[INFO] fastdeploy/vision/common/processors/transform.cc(159)::FuseNormalizeColorConvert BGR2RGB and NormalizeAndPermute are fused to NormalizeAndPermute with swap_rb=1
[INFO] fastdeploy/runtime/runtime.cc(328)::CreateLiteBackend    Runtime initialized with Backend::PDLITE in Device::KUNLUNXIN.
INFO:     Started server process [8076]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
register finished.
Load Model and Create API Cost Time: 87.98551559448242 ms
INFO:     127.0.0.1:41592 - "POST /predict HTTP/1.1" 200 OK
INFO:     127.0.0.1:40748 - "POST /predict HTTP/1.1" 200 OK
INFO:     127.0.0.1:57452 - "POST /predict HTTP/1.1" 200 OK
```

# 六、服务目录结构

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
```

