# 一、测试指令

> 注意将`model_path`设置为`bpu`模型的路径，并在同一级目录存放`model.yaml`的推理配置文件。

```bash
# 参数说明
# model_path: 模型存放路径
# params_path: 权重路径 —— pdmodel模型时必须
# model_type: 模型类型 —— cls、det、seg
# model_name: 模型名 —— 用于搜索接口，需要与注册的模型推理接口(注册别名)一致
# deploy_device: 推理设备 —— 可用于运行时配置，避免运行在错误的设备
# deploy_backend: 后端类型 —— 目前仅支持fastdeploy，后期自行扩展后可改为其它后端

bash test_server.sh --model_path package/model/model.pdmodel --params_path package/model/model.pdiparams --model_type cls --model_name mobilenetv1 --deploy_device npu --deploy_backend fastdeploy
```

------

# 二、服务状态/关闭指令

查看运行状态:

```bash
ps aux | grep uvicorn
#### 日志如下: ####
root         235 39.8  0.0 2376960 136128 pts/0  S    23:34   0:07 /usr/bin/python3.9 /usr/local/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1
root         308  0.0  0.0  11840  1920 pts/0    S+   23:34   0:00 grep --color=always uvicorn
```

查看运行日志:

```bash
cat server.log
#### 日志如下: ####
...
relu:batch_norm_23.tmp_2:relu_23.tmp_0
conv2d:conv2d_24.w_0,relu_23.tmp_0:conv2d_12.tmp_0
batch_norm:batch_norm2d_24.b_0,batch_norm2d_24.w_1,batch_norm2d_24.w_0,batch_norm2d_24.w_2,conv2d_12.tmp_0:batch_norm2d_24.w_1,batch_norm_24.tmp_0,batch_norm_24.tmp_1,batch_norm2d_24.w_2,batch_norm_24.tmp_2
relu:batch_norm_24.tmp_2:relu_24.tmp_0
depthwise_conv2d:conv2d_25.w_0,relu_24.tmp_0:depthwise_conv2d_12.tmp_0
batch_norm:batch_norm2d_25.b_0,batch_norm2d_25.w_1,batch_norm2d_25.w_0,batch_norm2d_25.w_2,depthwise_conv2d_12.tmp_0:batch_norm2d_25.w_1,batch_norm_25.tmp_0,batch_norm_25.tmp_1,batch_norm2d_25.w_2,batch_norm_25.tmp_2
relu:batch_norm_25.tmp_2:relu_25.tmp_0
conv2d:conv2d_26.w_0,relu_25.tmp_0:conv2d_13.tmp_0
batch_norm:batch_norm2d_26.b_0,batch_norm2d_26.w_1,batch_norm2d_26.w_0,batch_norm2d_26.w_2,conv2d_13.tmp_0:batch_norm2d_26.w_1,batch_norm_26.tmp_0,batch_norm_26.tmp_1,batch_norm2d_26.w_2,batch_norm_26.tmp_2
relu:batch_norm_26.tmp_2:relu_26.tmp_0
pool2d:relu_26.tmp_0:pool2d_0.tmp_0
flatten_contiguous_range:pool2d_0.tmp_0:flatten_0.tmp_0
matmul_v2:flatten_0.tmp_0,linear_0.w_0:linear_0.tmp_0
elementwise_add:linear_0.tmp_0,linear_0.b_0:save_infer_model/scale_0.tmp_0
fetch:save_infer_model/scale_0.tmp_0:fetch

[INFO] fastdeploy/runtime/runtime.cc(354)::CreateLiteBackend    Runtime initialized with Backend::PDLITE in Device::ASCEND.
INFO:     Started server process [235]
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
-F "file=@./ILSVRC2012_val_00000010.jpeg" \
-F "threshold=0.5" \
-F "topk=1"
```

运行结果1:

```bash
"{\"label_ids\": [5], \"scores\": [4.44921875]}"
```

------

测试指令2:

```bash
curl -X POST "http://localhost:8000/predict" \
-F "file=@./ILSVRC2012_val_00000010.jpeg" \
-F "threshold=0.5"
```

运行结果2:

```bash
"{\"label_ids\": [5], \"scores\": [4.44921875]}"
```

------

测试指令3:

```bash
curl -X POST "http://localhost:8000/predict" \
-F "file=@./ILSVRC2012_val_00000010.jpeg" \
-F "topk=5"
```

运行结果3:

```bash
"{\"label_ids\": [5, 8, 0, 9, 6], \"scores\": [4.44921875, 2.806640625, 0.677734375, 0.62744140625, 0.5361328125]}"
```

------

# 四、完整服务的测试运行日志

```bash
...
relu:batch_norm_26.tmp_2:relu_26.tmp_0
pool2d:relu_26.tmp_0:pool2d_0.tmp_0
flatten_contiguous_range:pool2d_0.tmp_0:flatten_0.tmp_0
matmul_v2:flatten_0.tmp_0,linear_0.w_0:linear_0.tmp_0
elementwise_add:linear_0.tmp_0,linear_0.b_0:save_infer_model/scale_0.tmp_0
fetch:save_infer_model/scale_0.tmp_0:fetch

[INFO] fastdeploy/runtime/runtime.cc(354)::CreateLiteBackend    Runtime initialized with Backend::PDLITE in Device::ASCEND.
INFO:     Started server process [114]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
register finished.
Load Model and Create API Cost Time: 244.5526123046875 ms
INFO:     127.0.0.1:11616 - "GET /health HTTP/1.1" 200 OK
[W  7/18 23:43: 1.816 .../src/driver/huawei_ascend_npu/utility.cc:57 InitializeAscendCL] CANN version mismatch. The build version is 0.0.0, but the current environment version is 5.1.2.
[I  7/18 23:43: 2.443 ...r/src/driver/huawei_ascend_npu/engine.cc:41 Context] properties:
[I  7/18 23:43: 2.443 ...r/src/driver/huawei_ascend_npu/engine.cc:66 Context] selected device ids:
[I  7/18 23:43: 2.443 ...r/src/driver/huawei_ascend_npu/engine.cc:68 Context] 0
[I  7/18 23:43: 2.443 ...r/src/driver/huawei_ascend_npu/engine.cc:78 Context] profiling path:
[I  7/18 23:43: 2.443 ...r/src/driver/huawei_ascend_npu/engine.cc:88 Context] dump model path:
[I  7/18 23:43: 2.443 ...r/src/driver/huawei_ascend_npu/engine.cc:98 Context] precision mode:
[I  7/18 23:43: 2.443 ...r/src/driver/huawei_ascend_npu/engine.cc:120 Context] op select impl mode:
[I  7/18 23:43: 2.443 ...r/src/driver/huawei_ascend_npu/engine.cc:130 Context] op type list for impl mode:
[I  7/18 23:43: 2.443 ...r/src/driver/huawei_ascend_npu/engine.cc:140 Context] enable compressw weight:
[I  7/18 23:43: 2.443 ...r/src/driver/huawei_ascend_npu/engine.cc:150 Context] auto tune mode:
[I  7/18 23:43: 2.443 ...r/src/driver/huawei_ascend_npu/engine.cc:160 Context] enable dynamic shape range:
[I  7/18 23:43: 2.443 ...r/src/driver/huawei_ascend_npu/engine.cc:176 Context] initial buffer length of dynamic shape range: -1
[W  7/18 23:43: 2.443 ...ter/nnadapter/src/runtime/compilation.cc:334 Finish] Warning: Failed to create a program, No model and cache is provided.
[W  7/18 23:43: 2.443 ...le-Lite/lite/kernels/nnadapter/engine.cc:149 LoadFromCache] Warning: Build model failed(3) !
[W  7/18 23:43: 2.452 ...nnadapter/nnadapter/src/runtime/model.cc:86 GetSupportedOperations] Warning: Failed to get the supported operations for device 'huawei_ascend_npu', because the HAL interface 'validate_program' is not implemented!
[W  7/18 23:43: 2.452 ...kernels/nnadapter/converter/converter.cc:171 Apply] Warning: Failed to get the supported operations for the selected devices, one or more of the selected devices are not supported!
[I  7/18 23:43: 2.452 ...r/src/driver/huawei_ascend_npu/driver.cc:70 CreateProgram] Create program for huawei_ascend_npu.
INFO:     127.0.0.1:11770 - "POST /predict HTTP/1.1" 200 OK
INFO:     127.0.0.1:14984 - "POST /predict HTTP/1.1" 200 OK
INFO:     127.0.0.1:15314 - "POST /predict HTTP/1.1" 200 OK
```

# 六、服务目录结构

```bash
- main.py # 服务启动代码，推理接口 `/predict` 接收: file, threshold, topk
- test_server.sh # 打包镜像前需自行测试目标接口是否可正常启动
- requirements.txt
- Dockerfile
- README.md
- ILSVRC2012_val_00000010.jpeg # 测试图片
- package/ # 自定义推理库
	- __init__.py # 引出Model供外部调用
	- deploymodel.py # 实现外部接口Model
	- backends.py # 整合fd等目录下后端的推理接口 —— 补充fastdeploy中api接口创建时指定模型类型为fastdeploy.ModelFormat.SOPHGO
	- base_option.py # 通用推理配置项基类
	- model/ # 存放模型目录
		- model.pdmodel # 存放paddle模型
		- model.pdiparams
		- model.yaml
	- fd/ # fastdeploy作为推理后端接口库——提供了基本的接口模板
		- __init__.py # 提供特定模型的推理接口
		- utils.py # 提供创建fastdeploy推理接口的创建函数，推理配置项的创建函数等 —— 检查option是否设置为有效参数
		- models.py # 注册各种模型的推理接口，具体结构可在该目录下自行实现后导入注册
```

