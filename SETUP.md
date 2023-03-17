# 安装系统

1. 下载旭日X3派系统镜像（桌面版）
    
    [链接：[https://pan.baidu.com/s/1whw8k4EVS4zKCaaBWOia_Q?pwd=snv2](https://pan.baidu.com/s/1whw8k4EVS4zKCaaBWOia_Q?pwd=snv2) ](https://developer.horizon.ai/resource)
    
    链接：[https://pan.baidu.com/s/1whw8k4EVS4zKCaaBWOia_Q?pwd=snv2](https://pan.baidu.com/s/1whw8k4EVS4zKCaaBWOia_Q?pwd=snv2) 
    
2. 利用balenaEtcher将下载得到的镜像文件烧写至SD卡
3. 启动系统
    
    保持旭日X3派开发板断电，将制作好的TF存储卡插入旭日X3派开发板的TF卡槽，并将显示器接入开发板HDMI接口，然后给开发板上电，用户可通过指示灯判断开发板状态，指示灯说明如下：
    
    - 红色指示灯：点亮代表硬件上电正常
    - 绿色指示灯：点亮代表系统启动中，熄灭代表系统启动完成
    
    系统首次启动时会安装镜像中预置的工具包，整个过程大概需要1分钟，完成后打开HDMI输出，并显示开机画面(Server系统显示地平线logo、Desktop版本显示系统桌面)。
    
    绿色指示灯熄灭，并且开机画面正常显示后，说明系统启动完成，此时可通过[串口登录](https://developer.horizon.ai/api/v1/fileData/documents_pi/Quick_Start/Quick_Start.html#login_uart)、[SSH登录](https://developer.horizon.ai/api/v1/fileData/documents_pi/Quick_Start/Quick_Start.html#ssh)方式登录开发板，登录用户名：`sunrise` 密码：`sunrise`
    

# 硬件设置

## 风扇使用

X3派自带的铝壳上有一个小风扇，风扇接线按下图所示接在40Pin接口的4、6端口上。风扇能看到标签的一面对应出风方向，应朝向芯片。

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/71caa1e0-943b-46fc-999a-f57cca5f0263/Untitled.png)

![微信图片_20221215163313.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/7816d2b9-d35e-4b4b-a1b1-231393beadc6/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20221215163313.png)

## WIFI天线

先将WIFI射频线D型端从铝壳孔中穿出，再将小端按压在主板上，最后将主板装在铝壳内。

## MIPI相机连接

![微信图片_20221215173137.jpg](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/6560d07f-a6c5-465d-a4d7-b6db9bc7a27c/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20221215173137.jpg)

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/7ab72804-3ca5-433a-aac9-7cd7fc3419f9/Untitled.png)

安装排线注意事项：

相机、主板接插件上都有一排黑色翻板卡扣，安装排线时需要先将卡扣打开；

相机端，蓝色片朝向相机背面；

主板端，蓝色片朝向主板正面；

```bash
cd /app/ai_inference/03_mipi_camera_sample/
sudo python3 ./mipi_camera.py
```

# 远程登录设置

在局域网内，通过一台Win笔记本，实现了经由WIFI的远程登录。主要需要配置Win电脑端的IPv4连接属性，将本机IP设为静态IP，网关设为255.255.255.0。X3派一端仅需连接到同一WIFI，不需要进行额外设置。X3派的IP地址可以通过路由器查看，设备名称为ubuntu。

使用MobaXterm软件，新建一个SSH连接，远程IP填写X3派IP，指定用户：sunrise，密码也为sunrise。能够成功登录。

# 模型部署

## 基本概念

在X3派上部署自定义模型涉及多项软件及其运行环境。从运行环境来说，包括：

1. 开发机（Ubuntu系统，实践中采用20.04）
2. X3派（Ubuntu系统）

在开发机上，需要下载并解压天工开物（也就是下文提到的OE）发布包、拉取OE开发环境镜像。X3派上不需要下载或拉取镜像，模型的部署都是通过开发机完成。

OE发布包是一个整合了各项资源，例如预训练模型等的资源包；OE镜像则包括模型部署所需的各项软件及其依赖的环境。

## 获取Open Explorer发布包

在以下链接：

[](https://developer.horizon.ai/forumDetail/136488103547258769)

下载**2.2.3 版本**的Open Explorer (简称OE)。运行以下命令进行下载：

```bash
# 下载发布包
wget -c ftp://vrftp.horizon.ai/Open_Explorer_gcc_9.3.0/2.2.3/horizon_xj3_open_explorer_v2.2.3a_20220701.tar.gz

# 下载文档（可选）
wget -c ftp://vrftp.horizon.ai/Open_Explorer_gcc_9.3.0/2.2.3/horizon_xj3_open_explorer_v2.2.3a_doc.zip
```

<aside>
⚠️ 直接点击链接下载无反应。官方提供的下载方式是通过wget，在Win端可通过MobaXterm内置的Terminal运行上述命令，然后再通过以下命令，将其从Moba内部地址移动到Win端：
mv horizon_xj3_open_explorer_v2.2.3a_doc.zip /drives/c/Users/dzp/Downloads/

</aside>

在Ubuntu开发机上，将发布包解压，得到 `horizon_xj3_open_explorer_v2.2.3a_20220701` 文件夹，其中内容包括：

```bash
.
├── bsp
├── ddk
├── doc
├── release_note.txt
├── run_docker.sh
└── tools
```

## 获取OE Docker镜像

使用以下命令从官方源拉取镜像：

```bash
docker pull openexplorer/ai_toolchain_centos_7_xj3:v2.3.3
```

<aside>
💡 OE开发包中的 `run_docker.sh` 脚本中内置了自动pull所需镜像的操作，因此可以不单独操作。但当所需镜像未在Docker Hub共享时，则需要单独下载镜像压缩包，并从官方提供的tar.gz中解压得到所需镜像，有必要的话还要对镜像重命名。
`docker load < docker_openexplorer_centos_7_xj3_v2.4.2.tar.gz`
`docker tag [hub.hobot.cc/aitools/ai_toolchain_centos_7_xj3:v2.4.2](http://hub.hobot.cc/aitools/ai_toolchain_centos_7_xj3:v2.4.2) openexplorer/ai_toolchain_centos_7_xj3:v2.4.2`

</aside>

<aside>
⚠️ 除了 `ai_toolchain_centos_7_xj3` 外，openexplorer还提供了 `ai_toolchain_ubuntu_gpu_xj3` ********， `ai_toolchain_centos_7` ， `ai_toolchain_ubuntu_gpu` 等镜像，但这些镜像均已停止维护。

</aside>

## 准备开发环境

[1. 产品介绍 - horizon_ai_toolchain_user_guide v1.12.3 文档](https://developer.horizon.ai/api/v1/fileData/doc/ddk_doc/navigation/ai_toolchain/docs_cn/horizon_ai_toolchain_user_guide/introduction.html)

在开发机端执行以下命令：

```bash
# 进入OE包顶层路径
cd horizon_xj3_open_explorer_v2.2.3a_20220701/

# 运行脚本启动CPU Docker容器，/data请在使用时替换为您校准/评测数据集路径
# 容器启动后，默认会将OE包挂载在/open_explorer，将数据集挂载在/data/horizon_x3/data
# data可以为新建文件夹，且可以使用相对路径，例如./data
bash run_docker.sh ./data
```

执行完成后会进入容器 `[root@40a4c5d5f2a7 open_explorer]#` ，使用 `ll` 命令查看根目录下内容，可以看到根目录内容与OE顶层文件夹内容一致。

## 板端环境配置

在容器内部根目录下运行以下命令：

```bash
cd /open_explorer/ddk/package/board

# board_ip是开发板局域网IP，例如192.168.31.90，可通过ping命令查看能否连接。
# 执行以下命令后需要输入密码以建立SSH连接，需要注意的是，建立连接的用户是root，密码也是root，而不是sunrise。安装过程中需要多次输入密码。
bash install.sh {board_ip}

# DZP: 以下内容在官方文档有涉及，但存在一些文件不存在类型的问题。且不做对部署自定义模型应该无影响
# cd /open_explorer
# scp -r ddk/samples/model_zoo/runtime/ root@{boad_ip}:/userdata/xj3/model/
# cd /userdata/xj3/script/00_quick_start/
# bash run_mobilenetV1.sh
```

<aside>
🚧 **scp: /userdata/xj3/model/: No such file or directory**
在上述运行过程中，scp如出现该问题，可以在开发机上通过Asbru（相当于Ubuntu端的MobaXterm）远程登录到X3派中，登录用户选择为root，在/userdata文件夹下创建缺失路径

</aside>

```bash
mkdir -p xj3/model
```

## 官方模型部署示例

本部分内容可参考模型转换示例包**（即：horizon_model_convert_sample）**手册：

[模型转换示例包手册 - horizon_model_convert_sample_documentation v1.12.3 文档](https://developer.horizon.ai/api/v1/fileData/doc/ddk_doc/navigation/ai_toolchain/docs_cn/hb_mapper_sample_doc/index.html)

官方提供的YOLOv3模型部署示例位于OE发布包 `ddk/samples/ai_toolchain/horizon_model_convert_sample/04_detection/02_yolov3_darknet53/mapper` 中。其中包括使用数字编号的脚本：

```bash
├── 01_check.sh
├── 02_preprocess.sh
├── 03_build.sh
├── 04_inference.sh
├── 05_evaluate.sh
```

其中01~04实际上正对应模型部署的完整流程，包括：

1. 模型检查
2. 校准数据预处理
3. 构建BPU用异构模型（模型转化）
4. 使用转化后的模型进行推理测试

在开发机OE镜像内部，依次运行上述脚本，理论上即可生成模型，其中最主要的是后缀为bin的模型文件。总体来说，为了运行该模型并实现相关功能，部署所需文件如下：

- Python库文件夹
- Python程序文件
- 模型bin文件
- coco_metric.py
- coco_classes.names

其中，黄色文件是参照上述流程生成的，绿色文件是已有的。黑色文件需要用户自行编写。上述文件置于同一文件夹内，可拷贝至开发板系统任意位置。在开发板上运行时，需要使用 `sudo` 。

<aside>
⚠️ 一些可能需要的依赖项：
sudo pip3 install EasyDict pycocotools

</aside>

### 模型检查

```bash
#!/usr/bin/env sh

set -e -v
cd $(dirname $0) || exit

model_type="caffe"
proto="../../../01_common/model_zoo/mapper/detection/yolov3_darknet53/yolov3_transposed.prototxt"
caffe_model="../../../01_common/model_zoo/mapper/detection/yolov3_darknet53/yolov3.caffemodel"
march="bernoulli2"

hb_mapper checker --model-type ${model_type} \
                  --proto ${proto} --model ${caffe_model} \
                  --march ${march}
```

### 校准数据预处理

```bash
#!/usr/bin/env bash

set -e -v
cd $(dirname $0) || exit

python3 ../../../data_preprocess.py \
  --src_dir ../../../01_common/calibration_data/coco \
  --dst_dir ./calibration_data_rgb_f32 \
  --pic_ext .rgb \
  --read_mode opencv
```

### 构建异构模型

```bash
#!/bin/bash

set -e -v
cd $(dirname $0)

config_file="./yolov3_darknet53_config.yaml"
model_type="caffe"
# build model
hb_mapper makertbin --config ${config_file} --model-type ${model_type}
```

<aside>
💡 上述脚本使用 `hb_mapper` 工具转换模型，最需要关注的是转换的配置文件， 请参考文档包 [Horizon AI Toolchain User Guide](https://developer.horizon.ai/api/v1/fileData/doc/ddk_doc/navigation/ai_toolchain/docs_cn/horizon_ai_toolchain_user_guide/model_conversion.html#hb-mapper-makertbin) 文档中《使用 hb_mapper makertbin 工具转换模型》内容。

</aside>

### 推理测试

```bash
#!/bin/bash

set -e -v
cd $(dirname $0)

#for converted quanti model inference
quanti_model_file="./model_output/yolov3_darknet53_416x416_nv12_quantized_model.onnx"
quanti_input_layout="NHWC"

#for original float model inference
original_model_file="./model_output/yolov3_darknet53_416x416_nv12_original_float_model.onnx"
original_input_layout="NCHW"

if [[ $1 =~ "origin" ]];  then
  model=$original_model_file
  layout=$original_input_layout
  input_offset=128
else
  model=$quanti_model_file
  layout=$quanti_input_layout
  input_offset=128  
fi

infer_image="../../../01_common/test_data/det_images/kite.jpg"

# -----------------------------------------------------------------------------------------------------
# shell command "sh 04_inference.sh" runs quanti inference by default 
# If quanti model infer is intended, please run the shell via command "sh 04_inference.sh quanti"
# If float model infer is intended, please run the shell via command "sh 04_inference.sh origin"
# -----------------------------------------------------------------------------------------------------

python3 -u ../../det_inference.py \
        --model ${model} \
        --image ${infer_image} \
        --input_layout ${layout} \
        --input_offset ${input_offset}
```

# 自定义模型部署

X3开发板的真正价值是部署并运行我们自己开发的AI模型。以下说明如何部署自定义模型。模型结构采用yolov5，部署的关键是将yolov5模型由PyTorch的pt格式转换为ONNX格式后，再转换为X3支持的格式。

[](https://developer.horizon.ai/forumDetail/112555549341653639)

## 获取YOLOv5

```bash
git clone https://github.com/ultralytics/yolov5
```

### YOLOv5快速运行验证

可通过以下示例检查yolov5是否正常工作，各依赖项是否成功安装：

```bash
python detect.py --weights ./models/yolov5s.pt --source 0
```

## 根据官方指引配置模型转换过程

地平线官方示例中使用的yolov5为该软件仓库中 `tag` 为 `v2.0` 的版本：

[2. 算法模型示例 - horizon_model_convert_sample_documentation v1.12.3 文档](https://developer.horizon.ai/api/v1/fileData/doc/ddk_doc/navigation/ai_toolchain/docs_cn/hb_mapper_sample_doc/samples/algorithm_sample.html#yolov5s)

**ATTENTION:对于yolov3模型，使用下面的更改方法，会由于维度不匹配报错。**

```bash
Traceback (most recent call last):
  File "train.py", line 635, in <module>
    main(opt)
  File "train.py", line 528, in main
    train(opt.hyp, opt, device, callbacks)
  File "train.py", line 310, in train
    loss, loss_items = compute_loss(pred, targets.to(device))  # loss scaled by batch_size
  File "/home/clover/yolov3/utils/loss.py", line 135, in __call__
    pxy, pwh, _, pcls = pi[b, a, gj, gi].split((2, 2, 1, self.nc), 1)  # target-subset of predictions
  File "/home/clover/.yolov3/lib/python3.8/site-packages/torch/_tensor.py", line 611, in split
    return super(Tensor, self).split_with_sizes(split_size, dim)
IndexError: Dimension out of range (expected to be in range of [-1, 0], but got 1)
```

地平线针对该版本，在ONNX模型导出前对Github代码做了如下修改 （代码参见：[https://github.com/ultralytics/yolov5/blob/v2.0/models/yolo.py](https://github.com/ultralytics/yolov5/blob/v2.0/models/yolo.py)）：

```bash
def forward(self, x):
    # x = x.copy()  # for profiling
    z = []  # inference output
    self.training |= self.export
    for i in range(self.nl):
        x[i] = self.m[i](x[i])  # conv
        bs, _, ny, nx = x[i].shape  # x(bs,255,20,20) to x(bs,3,20,20,85)
        # x[i] = x[i].view(bs, self.na, self.no, ny, nx).permute(0, 1, 3, 4, 2).contiguous()
        x[i] = x[i].permute(0, 2, 3, 1).contiguous()
```

即将原本的5维输出改为4维，不拆分 `anchor size (3)` 和 `info size (85)` ，而是将两者合并，视为通道 `C (255)` 并后置。这样做的原因是，[BPU的输出只能是4维的数据](https://developer.horizon.ai/forumDetail/106482341031036103)。

该版本 `forward` 代码中本来还有以下标黄内容，经过调试发现，该版本在 `export` 脚本运行时 `self.training` 变量为 `True` ，因此标黄部分根本不会运行， `x` 就是模型的最终输出，这样也不难理解相对应的后处理代码出现在地平线官方提供的例程中。

```python
def forward(self, x):
    # x = x.copy()  # for profiling
    z = []  # inference output
    self.training |= self.export
    for i in range(self.nl):
        x[i] = self.m[i](x[i])  # conv
        bs, _, ny, nx = x[i].shape  # x(bs,255,20,20) to x(bs,3,20,20,85)
        # x[i] = x[i].view(bs, self.na, self.no, ny, nx).permute(0, 1, 3, 4, 2).contiguous()
        x[i] = x[i].permute(0, 2, 3, 1).contiguous()

        if not self.training:  # inference
            if self.grid[i].shape[2:4] != x[i].shape[2:4]:
                self.grid[i] = self._make_grid(nx, ny).to(x[i].device)

            y = x[i].sigmoid()
            y[..., 0:2] = (y[..., 0:2] * 2. - 0.5 + self.grid[i].to(x[i].device)) * self.stride[i]  # xy
            y[..., 2:4] = (y[..., 2:4] * 2) ** 2 * self.anchor_grid[i]  # wh
            z.append(y.view(bs, -1, self.no))

    return x if self.training else (torch.cat(z, 1), x)
```

<aside>
🚧 使用官方推荐的v2.0版本进行如上操作，会由于PyTorch版本问题报以下错误：

[https://github.com/ultralytics/yolov5/issues/6948](https://github.com/ultralytics/yolov5/issues/6948)

具体报错信息如下：

```bash
Traceback (most recent call last):
  File "models/export.py", line 29, in <module>
    y = model(img)  # dry run
  File "/home/dzp/.local/lib/python3.8/site-packages/torch/nn/modules/module.py", line 1130, in _call_impl
    return forward_call(*input, **kwargs)
  File "/home/dzp/yolov5/models/yolo.py", line 99, in forward
    return self.forward_once(x, profile)  # single-scale inference, train
  File "/home/dzp/yolov5/models/yolo.py", line 119, in forward_once
    x = m(x)  # run
  File "/home/dzp/.local/lib/python3.8/site-packages/torch/nn/modules/module.py", line 1130, in _call_impl
    return forward_call(*input, **kwargs)
  File "/home/dzp/.local/lib/python3.8/site-packages/torch/nn/modules/upsampling.py", line 154, in forward
    recompute_scale_factor=self.recompute_scale_factor)
  File "/home/dzp/.local/lib/python3.8/site-packages/torch/nn/modules/module.py", line 1207, in __getattr__
    raise AttributeError("'{}' object has no attribute '{}'".format(
AttributeError: 'Upsample' object has no attribute 'recompute_scale_factor'
```

不过，该问题的修复方式相对简单（针对 torch 1.12.1），方法为，将 `torch/nn/modules/upsampling.py` 154行代码更改为：

```bash
def forward(self, input: Tensor) -> Tensor:
    # return F.interpolate(input, self.size, self.scale_factor, self.mode, self.align_corners,
    #                      recompute_scale_factor=self.recompute_scale_factor)
    return F.interpolate(input, self.size, self.scale_factor, self.mode, self.align_corners)
```

该改动的潜在隐患目前未知。

</aside>

## PT转ONNX（v2.0版）

在解决上述问题后，按官方指引修改 `export.py` 文件，运行结果如下：

- `export PYTHONPATH="$PWD" && python models/export.py` 运行于 `yolov5` 根目录下（未修改yolo.py）
    
    ```bash
    Namespace(batch_size=1, img_size=[672, 672], weights='./weights/yolov5s.pt')
    
    Starting TorchScript export with torch 1.12.1+cu116...
    /home/dzp/.local/lib/python3.8/site-packages/torch/jit/_trace.py:967: TracerWarning: Encountering a list at the output of the tracer might cause the trace to be incorrect, this is only valid if the container structure does not change based on the module's inputs. Consider using a constant container instead (e.g. for `list`, use a `tuple` instead. for `dict`, use a `NamedTuple` instead). If you absolutely need this and know the side effects, pass strict=False to trace() to allow this behavior.
      module._c._create_method_from_trace(
    TorchScript export success, saved as ./weights/yolov5s.torchscript.pt
    
    Starting ONNX export with onnx 1.12.0...
    Fusing layers... Model Summary: 140 layers, 7.45958e+06 parameters, 6.61683e+06 gradients, 17.4 GFLOPS
    /home/dzp/yolov5/models/yolo.py:83: TracerWarning: Converting a tensor to a Python boolean might cause the trace to be incorrect. We can't record the data flow of Python values, so this value will be treated as a constant in the future. This means that the trace might not generalize to other inputs!
      if augment:
    /home/dzp/yolov5/models/yolo.py:107: TracerWarning: Converting a tensor to a Python boolean might cause the trace to be incorrect. We can't record the data flow of Python values, so this value will be treated as a constant in the future. This means that the trace might not generalize to other inputs!
      if profile:
    /home/dzp/yolov5/models/yolo.py:122: TracerWarning: Converting a tensor to a Python boolean might cause the trace to be incorrect. We can't record the data flow of Python values, so this value will be treated as a constant in the future. This means that the trace might not generalize to other inputs!
      if profile:
    graph torch_jit (
      %data[FLOAT, 1x3x672x672]
    ) initializers (
      %model.0.conv.conv.weight[FLOAT, 32x12x3x3]
      %model.0.conv.conv.bias[FLOAT, 32]
      %model.1.conv.weight[FLOAT, 64x32x3x3]
      %model.1.conv.bias[FLOAT, 64]
      %model.2.cv1.conv.weight[FLOAT, 32x64x1x1]
      %model.2.cv1.conv.bias[FLOAT, 32]
      %model.2.cv2.weight[FLOAT, 32x64x1x1]
      %model.2.cv3.weight[FLOAT, 32x32x1x1]
      %model.2.cv4.conv.weight[FLOAT, 64x64x1x1]
      %model.2.cv4.conv.bias[FLOAT, 64]
      %model.2.bn.weight[FLOAT, 64]
      %model.2.bn.bias[FLOAT, 64]
      %model.2.bn.running_mean[FLOAT, 64]
      %model.2.bn.running_var[FLOAT, 64]
      %model.2.m.0.cv1.conv.weight[FLOAT, 32x32x1x1]
      %model.2.m.0.cv1.conv.bias[FLOAT, 32]
      %model.2.m.0.cv2.conv.weight[FLOAT, 32x32x3x3]
      %model.2.m.0.cv2.conv.bias[FLOAT, 32]
      %model.3.conv.weight[FLOAT, 128x64x3x3]
      %model.3.conv.bias[FLOAT, 128]
      %model.4.cv1.conv.weight[FLOAT, 64x128x1x1]
      %model.4.cv1.conv.bias[FLOAT, 64]
      %model.4.cv2.weight[FLOAT, 64x128x1x1]
      %model.4.cv3.weight[FLOAT, 64x64x1x1]
      %model.4.cv4.conv.weight[FLOAT, 128x128x1x1]
      %model.4.cv4.conv.bias[FLOAT, 128]
      %model.4.bn.weight[FLOAT, 128]
      %model.4.bn.bias[FLOAT, 128]
      %model.4.bn.running_mean[FLOAT, 128]
      %model.4.bn.running_var[FLOAT, 128]
      %model.4.m.0.cv1.conv.weight[FLOAT, 64x64x1x1]
      %model.4.m.0.cv1.conv.bias[FLOAT, 64]
      %model.4.m.0.cv2.conv.weight[FLOAT, 64x64x3x3]
      %model.4.m.0.cv2.conv.bias[FLOAT, 64]
      %model.4.m.1.cv1.conv.weight[FLOAT, 64x64x1x1]
      %model.4.m.1.cv1.conv.bias[FLOAT, 64]
      %model.4.m.1.cv2.conv.weight[FLOAT, 64x64x3x3]
      %model.4.m.1.cv2.conv.bias[FLOAT, 64]
      %model.4.m.2.cv1.conv.weight[FLOAT, 64x64x1x1]
      %model.4.m.2.cv1.conv.bias[FLOAT, 64]
      %model.4.m.2.cv2.conv.weight[FLOAT, 64x64x3x3]
      %model.4.m.2.cv2.conv.bias[FLOAT, 64]
      %model.5.conv.weight[FLOAT, 256x128x3x3]
      %model.5.conv.bias[FLOAT, 256]
      %model.6.cv1.conv.weight[FLOAT, 128x256x1x1]
      %model.6.cv1.conv.bias[FLOAT, 128]
      %model.6.cv2.weight[FLOAT, 128x256x1x1]
      %model.6.cv3.weight[FLOAT, 128x128x1x1]
      %model.6.cv4.conv.weight[FLOAT, 256x256x1x1]
      %model.6.cv4.conv.bias[FLOAT, 256]
      %model.6.bn.weight[FLOAT, 256]
      %model.6.bn.bias[FLOAT, 256]
      %model.6.bn.running_mean[FLOAT, 256]
      %model.6.bn.running_var[FLOAT, 256]
      %model.6.m.0.cv1.conv.weight[FLOAT, 128x128x1x1]
      %model.6.m.0.cv1.conv.bias[FLOAT, 128]
      %model.6.m.0.cv2.conv.weight[FLOAT, 128x128x3x3]
      %model.6.m.0.cv2.conv.bias[FLOAT, 128]
      %model.6.m.1.cv1.conv.weight[FLOAT, 128x128x1x1]
      %model.6.m.1.cv1.conv.bias[FLOAT, 128]
      %model.6.m.1.cv2.conv.weight[FLOAT, 128x128x3x3]
      %model.6.m.1.cv2.conv.bias[FLOAT, 128]
      %model.6.m.2.cv1.conv.weight[FLOAT, 128x128x1x1]
      %model.6.m.2.cv1.conv.bias[FLOAT, 128]
      %model.6.m.2.cv2.conv.weight[FLOAT, 128x128x3x3]
      %model.6.m.2.cv2.conv.bias[FLOAT, 128]
      %model.7.conv.weight[FLOAT, 512x256x3x3]
      %model.7.conv.bias[FLOAT, 512]
      %model.8.cv1.conv.weight[FLOAT, 256x512x1x1]
      %model.8.cv1.conv.bias[FLOAT, 256]
      %model.8.cv2.conv.weight[FLOAT, 512x1024x1x1]
      %model.8.cv2.conv.bias[FLOAT, 512]
      %model.9.cv1.conv.weight[FLOAT, 256x512x1x1]
      %model.9.cv1.conv.bias[FLOAT, 256]
      %model.9.cv2.weight[FLOAT, 256x512x1x1]
      %model.9.cv3.weight[FLOAT, 256x256x1x1]
      %model.9.cv4.conv.weight[FLOAT, 512x512x1x1]
      %model.9.cv4.conv.bias[FLOAT, 512]
      %model.9.bn.weight[FLOAT, 512]
      %model.9.bn.bias[FLOAT, 512]
      %model.9.bn.running_mean[FLOAT, 512]
      %model.9.bn.running_var[FLOAT, 512]
      %model.9.m.0.cv1.conv.weight[FLOAT, 256x256x1x1]
      %model.9.m.0.cv1.conv.bias[FLOAT, 256]
      %model.9.m.0.cv2.conv.weight[FLOAT, 256x256x3x3]
      %model.9.m.0.cv2.conv.bias[FLOAT, 256]
      %model.10.conv.weight[FLOAT, 256x512x1x1]
      %model.10.conv.bias[FLOAT, 256]
      %model.13.cv1.conv.weight[FLOAT, 128x512x1x1]
      %model.13.cv1.conv.bias[FLOAT, 128]
      %model.13.cv2.weight[FLOAT, 128x512x1x1]
      %model.13.cv3.weight[FLOAT, 128x128x1x1]
      %model.13.cv4.conv.weight[FLOAT, 256x256x1x1]
      %model.13.cv4.conv.bias[FLOAT, 256]
      %model.13.bn.weight[FLOAT, 256]
      %model.13.bn.bias[FLOAT, 256]
      %model.13.bn.running_mean[FLOAT, 256]
      %model.13.bn.running_var[FLOAT, 256]
      %model.13.m.0.cv1.conv.weight[FLOAT, 128x128x1x1]
      %model.13.m.0.cv1.conv.bias[FLOAT, 128]
      %model.13.m.0.cv2.conv.weight[FLOAT, 128x128x3x3]
      %model.13.m.0.cv2.conv.bias[FLOAT, 128]
      %model.14.conv.weight[FLOAT, 128x256x1x1]
      %model.14.conv.bias[FLOAT, 128]
      %model.17.cv1.conv.weight[FLOAT, 64x256x1x1]
      %model.17.cv1.conv.bias[FLOAT, 64]
      %model.17.cv2.weight[FLOAT, 64x256x1x1]
      %model.17.cv3.weight[FLOAT, 64x64x1x1]
      %model.17.cv4.conv.weight[FLOAT, 128x128x1x1]
      %model.17.cv4.conv.bias[FLOAT, 128]
      %model.17.bn.weight[FLOAT, 128]
      %model.17.bn.bias[FLOAT, 128]
      %model.17.bn.running_mean[FLOAT, 128]
      %model.17.bn.running_var[FLOAT, 128]
      %model.17.m.0.cv1.conv.weight[FLOAT, 64x64x1x1]
      %model.17.m.0.cv1.conv.bias[FLOAT, 64]
      %model.17.m.0.cv2.conv.weight[FLOAT, 64x64x3x3]
      %model.17.m.0.cv2.conv.bias[FLOAT, 64]
      %model.18.conv.weight[FLOAT, 128x128x3x3]
      %model.18.conv.bias[FLOAT, 128]
      %model.20.cv1.conv.weight[FLOAT, 128x256x1x1]
      %model.20.cv1.conv.bias[FLOAT, 128]
      %model.20.cv2.weight[FLOAT, 128x256x1x1]
      %model.20.cv3.weight[FLOAT, 128x128x1x1]
      %model.20.cv4.conv.weight[FLOAT, 256x256x1x1]
      %model.20.cv4.conv.bias[FLOAT, 256]
      %model.20.bn.weight[FLOAT, 256]
      %model.20.bn.bias[FLOAT, 256]
      %model.20.bn.running_mean[FLOAT, 256]
      %model.20.bn.running_var[FLOAT, 256]
      %model.20.m.0.cv1.conv.weight[FLOAT, 128x128x1x1]
      %model.20.m.0.cv1.conv.bias[FLOAT, 128]
      %model.20.m.0.cv2.conv.weight[FLOAT, 128x128x3x3]
      %model.20.m.0.cv2.conv.bias[FLOAT, 128]
      %model.21.conv.weight[FLOAT, 256x256x3x3]
      %model.21.conv.bias[FLOAT, 256]
      %model.23.cv1.conv.weight[FLOAT, 256x512x1x1]
      %model.23.cv1.conv.bias[FLOAT, 256]
      %model.23.cv2.weight[FLOAT, 256x512x1x1]
      %model.23.cv3.weight[FLOAT, 256x256x1x1]
      %model.23.cv4.conv.weight[FLOAT, 512x512x1x1]
      %model.23.cv4.conv.bias[FLOAT, 512]
      %model.23.bn.weight[FLOAT, 512]
      %model.23.bn.bias[FLOAT, 512]
      %model.23.bn.running_mean[FLOAT, 512]
      %model.23.bn.running_var[FLOAT, 512]
      %model.23.m.0.cv1.conv.weight[FLOAT, 256x256x1x1]
      %model.23.m.0.cv1.conv.bias[FLOAT, 256]
      %model.23.m.0.cv2.conv.weight[FLOAT, 256x256x3x3]
      %model.23.m.0.cv2.conv.bias[FLOAT, 256]
      %model.24.m.0.weight[FLOAT, 255x128x1x1]
      %model.24.m.0.bias[FLOAT, 255]
      %model.24.m.1.weight[FLOAT, 255x256x1x1]
      %model.24.m.1.bias[FLOAT, 255]
      %model.24.m.2.weight[FLOAT, 255x512x1x1]
      %model.24.m.2.bias[FLOAT, 255]
      %onnx::Resize_419[FLOAT, 4]
      %onnx::Reshape_426[INT64, 5]
      %onnx::Reshape_432[INT64, 5]
      %onnx::Reshape_438[INT64, 5]
    ) {
      %onnx::Resize_420 = Identity(%onnx::Resize_419)
      %onnx::Slice_169 = Constant[value = <Tensor>]()
      %onnx::Slice_170 = Constant[value = <Tensor>]()
      %onnx::Slice_171 = Constant[value = <Tensor>]()
      %onnx::Slice_172 = Constant[value = <Tensor>]()
      %onnx::Slice_173 = Slice(%data, %onnx::Slice_170, %onnx::Slice_171, %onnx::Slice_169, %onnx::Slice_172)
      %onnx::Slice_174 = Constant[value = <Tensor>]()
      %onnx::Slice_175 = Constant[value = <Tensor>]()
      %onnx::Slice_176 = Constant[value = <Tensor>]()
      %onnx::Slice_177 = Constant[value = <Tensor>]()
      %onnx::Concat_178 = Slice(%onnx::Slice_173, %onnx::Slice_175, %onnx::Slice_176, %onnx::Slice_174, %onnx::Slice_177)
      %onnx::Slice_179 = Constant[value = <Tensor>]()
      %onnx::Slice_180 = Constant[value = <Tensor>]()
      %onnx::Slice_181 = Constant[value = <Tensor>]()
      %onnx::Slice_182 = Constant[value = <Tensor>]()
      %onnx::Slice_183 = Slice(%data, %onnx::Slice_180, %onnx::Slice_181, %onnx::Slice_179, %onnx::Slice_182)
      %onnx::Slice_184 = Constant[value = <Tensor>]()
      %onnx::Slice_185 = Constant[value = <Tensor>]()
      %onnx::Slice_186 = Constant[value = <Tensor>]()
      %onnx::Slice_187 = Constant[value = <Tensor>]()
      %onnx::Concat_188 = Slice(%onnx::Slice_183, %onnx::Slice_185, %onnx::Slice_186, %onnx::Slice_184, %onnx::Slice_187)
      %onnx::Slice_189 = Constant[value = <Tensor>]()
      %onnx::Slice_190 = Constant[value = <Tensor>]()
      %onnx::Slice_191 = Constant[value = <Tensor>]()
      %onnx::Slice_192 = Constant[value = <Tensor>]()
      %onnx::Slice_193 = Slice(%data, %onnx::Slice_190, %onnx::Slice_191, %onnx::Slice_189, %onnx::Slice_192)
      %onnx::Slice_194 = Constant[value = <Tensor>]()
      %onnx::Slice_195 = Constant[value = <Tensor>]()
      %onnx::Slice_196 = Constant[value = <Tensor>]()
      %onnx::Slice_197 = Constant[value = <Tensor>]()
      %onnx::Concat_198 = Slice(%onnx::Slice_193, %onnx::Slice_195, %onnx::Slice_196, %onnx::Slice_194, %onnx::Slice_197)
      %onnx::Slice_199 = Constant[value = <Tensor>]()
      %onnx::Slice_200 = Constant[value = <Tensor>]()
      %onnx::Slice_201 = Constant[value = <Tensor>]()
      %onnx::Slice_202 = Constant[value = <Tensor>]()
      %onnx::Slice_203 = Slice(%data, %onnx::Slice_200, %onnx::Slice_201, %onnx::Slice_199, %onnx::Slice_202)
      %onnx::Slice_204 = Constant[value = <Tensor>]()
      %onnx::Slice_205 = Constant[value = <Tensor>]()
      %onnx::Slice_206 = Constant[value = <Tensor>]()
      %onnx::Slice_207 = Constant[value = <Tensor>]()
      %onnx::Concat_208 = Slice(%onnx::Slice_203, %onnx::Slice_205, %onnx::Slice_206, %onnx::Slice_204, %onnx::Slice_207)
      %input = Concat[axis = 1](%onnx::Concat_178, %onnx::Concat_188, %onnx::Concat_198, %onnx::Concat_208)
      %input.3 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [1, 1]](%input, %model.0.conv.conv.weight, %model.0.conv.conv.bias)
      %onnx::Conv_211 = LeakyRelu[alpha = 0.100000001490116](%input.3)
      %input.7 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [2, 2]](%onnx::Conv_211, %model.1.conv.weight, %model.1.conv.bias)
      %onnx::Conv_213 = LeakyRelu[alpha = 0.100000001490116](%input.7)
      %input.11 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_213, %model.2.cv1.conv.weight, %model.2.cv1.conv.bias)
      %onnx::Conv_215 = LeakyRelu[alpha = 0.100000001490116](%input.11)
      %input.15 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_215, %model.2.m.0.cv1.conv.weight, %model.2.m.0.cv1.conv.bias)
      %onnx::Conv_217 = LeakyRelu[alpha = 0.100000001490116](%input.15)
      %input.19 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [1, 1]](%onnx::Conv_217, %model.2.m.0.cv2.conv.weight, %model.2.m.0.cv2.conv.bias)
      %onnx::Add_219 = LeakyRelu[alpha = 0.100000001490116](%input.19)
      %input.23 = Add(%onnx::Conv_215, %onnx::Add_219)
      %onnx::Concat_221 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%input.23, %model.2.cv3.weight)
      %onnx::Concat_222 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_213, %model.2.cv2.weight)
      %input.27 = Concat[axis = 1](%onnx::Concat_221, %onnx::Concat_222)
      %input.31 = BatchNormalization[epsilon = 0.00100000004749745, momentum = 0.990000009536743](%input.27, %model.2.bn.weight, %model.2.bn.bias, %model.2.bn.running_mean, %model.2.bn.running_var)
      %onnx::Conv_225 = LeakyRelu[alpha = 0.100000001490116](%input.31)
      %input.35 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_225, %model.2.cv4.conv.weight, %model.2.cv4.conv.bias)
      %onnx::Conv_227 = LeakyRelu[alpha = 0.100000001490116](%input.35)
      %input.39 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [2, 2]](%onnx::Conv_227, %model.3.conv.weight, %model.3.conv.bias)
      %onnx::Conv_229 = LeakyRelu[alpha = 0.100000001490116](%input.39)
      %input.43 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_229, %model.4.cv1.conv.weight, %model.4.cv1.conv.bias)
      %onnx::Conv_231 = LeakyRelu[alpha = 0.100000001490116](%input.43)
      %input.47 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_231, %model.4.m.0.cv1.conv.weight, %model.4.m.0.cv1.conv.bias)
      %onnx::Conv_233 = LeakyRelu[alpha = 0.100000001490116](%input.47)
      %input.51 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [1, 1]](%onnx::Conv_233, %model.4.m.0.cv2.conv.weight, %model.4.m.0.cv2.conv.bias)
      %onnx::Add_235 = LeakyRelu[alpha = 0.100000001490116](%input.51)
      %input.55 = Add(%onnx::Conv_231, %onnx::Add_235)
      %input.59 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%input.55, %model.4.m.1.cv1.conv.weight, %model.4.m.1.cv1.conv.bias)
      %onnx::Conv_238 = LeakyRelu[alpha = 0.100000001490116](%input.59)
      %input.63 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [1, 1]](%onnx::Conv_238, %model.4.m.1.cv2.conv.weight, %model.4.m.1.cv2.conv.bias)
      %onnx::Add_240 = LeakyRelu[alpha = 0.100000001490116](%input.63)
      %input.67 = Add(%input.55, %onnx::Add_240)
      %input.71 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%input.67, %model.4.m.2.cv1.conv.weight, %model.4.m.2.cv1.conv.bias)
      %onnx::Conv_243 = LeakyRelu[alpha = 0.100000001490116](%input.71)
      %input.75 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [1, 1]](%onnx::Conv_243, %model.4.m.2.cv2.conv.weight, %model.4.m.2.cv2.conv.bias)
      %onnx::Add_245 = LeakyRelu[alpha = 0.100000001490116](%input.75)
      %input.79 = Add(%input.67, %onnx::Add_245)
      %onnx::Concat_247 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%input.79, %model.4.cv3.weight)
      %onnx::Concat_248 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_229, %model.4.cv2.weight)
      %input.83 = Concat[axis = 1](%onnx::Concat_247, %onnx::Concat_248)
      %input.87 = BatchNormalization[epsilon = 0.00100000004749745, momentum = 0.990000009536743](%input.83, %model.4.bn.weight, %model.4.bn.bias, %model.4.bn.running_mean, %model.4.bn.running_var)
      %onnx::Conv_251 = LeakyRelu[alpha = 0.100000001490116](%input.87)
      %input.91 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_251, %model.4.cv4.conv.weight, %model.4.cv4.conv.bias)
      %onnx::Conv_253 = LeakyRelu[alpha = 0.100000001490116](%input.91)
      %input.95 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [2, 2]](%onnx::Conv_253, %model.5.conv.weight, %model.5.conv.bias)
      %onnx::Conv_255 = LeakyRelu[alpha = 0.100000001490116](%input.95)
      %input.99 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_255, %model.6.cv1.conv.weight, %model.6.cv1.conv.bias)
      %onnx::Conv_257 = LeakyRelu[alpha = 0.100000001490116](%input.99)
      %input.103 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_257, %model.6.m.0.cv1.conv.weight, %model.6.m.0.cv1.conv.bias)
      %onnx::Conv_259 = LeakyRelu[alpha = 0.100000001490116](%input.103)
      %input.107 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [1, 1]](%onnx::Conv_259, %model.6.m.0.cv2.conv.weight, %model.6.m.0.cv2.conv.bias)
      %onnx::Add_261 = LeakyRelu[alpha = 0.100000001490116](%input.107)
      %input.111 = Add(%onnx::Conv_257, %onnx::Add_261)
      %input.115 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%input.111, %model.6.m.1.cv1.conv.weight, %model.6.m.1.cv1.conv.bias)
      %onnx::Conv_264 = LeakyRelu[alpha = 0.100000001490116](%input.115)
      %input.119 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [1, 1]](%onnx::Conv_264, %model.6.m.1.cv2.conv.weight, %model.6.m.1.cv2.conv.bias)
      %onnx::Add_266 = LeakyRelu[alpha = 0.100000001490116](%input.119)
      %input.123 = Add(%input.111, %onnx::Add_266)
      %input.127 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%input.123, %model.6.m.2.cv1.conv.weight, %model.6.m.2.cv1.conv.bias)
      %onnx::Conv_269 = LeakyRelu[alpha = 0.100000001490116](%input.127)
      %input.131 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [1, 1]](%onnx::Conv_269, %model.6.m.2.cv2.conv.weight, %model.6.m.2.cv2.conv.bias)
      %onnx::Add_271 = LeakyRelu[alpha = 0.100000001490116](%input.131)
      %input.135 = Add(%input.123, %onnx::Add_271)
      %onnx::Concat_273 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%input.135, %model.6.cv3.weight)
      %onnx::Concat_274 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_255, %model.6.cv2.weight)
      %input.139 = Concat[axis = 1](%onnx::Concat_273, %onnx::Concat_274)
      %input.143 = BatchNormalization[epsilon = 0.00100000004749745, momentum = 0.990000009536743](%input.139, %model.6.bn.weight, %model.6.bn.bias, %model.6.bn.running_mean, %model.6.bn.running_var)
      %onnx::Conv_277 = LeakyRelu[alpha = 0.100000001490116](%input.143)
      %input.147 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_277, %model.6.cv4.conv.weight, %model.6.cv4.conv.bias)
      %onnx::Conv_279 = LeakyRelu[alpha = 0.100000001490116](%input.147)
      %input.151 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [2, 2]](%onnx::Conv_279, %model.7.conv.weight, %model.7.conv.bias)
      %onnx::Conv_281 = LeakyRelu[alpha = 0.100000001490116](%input.151)
      %input.155 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_281, %model.8.cv1.conv.weight, %model.8.cv1.conv.bias)
      %onnx::MaxPool_283 = LeakyRelu[alpha = 0.100000001490116](%input.155)
      %onnx::Concat_284 = MaxPool[ceil_mode = 0, kernel_shape = [5, 5], pads = [2, 2, 2, 2], strides = [1, 1]](%onnx::MaxPool_283)
      %onnx::Concat_285 = MaxPool[ceil_mode = 0, kernel_shape = [9, 9], pads = [4, 4, 4, 4], strides = [1, 1]](%onnx::MaxPool_283)
      %onnx::Concat_286 = MaxPool[ceil_mode = 0, kernel_shape = [13, 13], pads = [6, 6, 6, 6], strides = [1, 1]](%onnx::MaxPool_283)
      %input.159 = Concat[axis = 1](%onnx::MaxPool_283, %onnx::Concat_284, %onnx::Concat_285, %onnx::Concat_286)
      %input.163 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%input.159, %model.8.cv2.conv.weight, %model.8.cv2.conv.bias)
      %onnx::Conv_289 = LeakyRelu[alpha = 0.100000001490116](%input.163)
      %input.167 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_289, %model.9.cv1.conv.weight, %model.9.cv1.conv.bias)
      %onnx::Conv_291 = LeakyRelu[alpha = 0.100000001490116](%input.167)
      %input.171 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_291, %model.9.m.0.cv1.conv.weight, %model.9.m.0.cv1.conv.bias)
      %onnx::Conv_293 = LeakyRelu[alpha = 0.100000001490116](%input.171)
      %input.175 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [1, 1]](%onnx::Conv_293, %model.9.m.0.cv2.conv.weight, %model.9.m.0.cv2.conv.bias)
      %onnx::Conv_295 = LeakyRelu[alpha = 0.100000001490116](%input.175)
      %onnx::Concat_296 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_295, %model.9.cv3.weight)
      %onnx::Concat_297 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_289, %model.9.cv2.weight)
      %input.179 = Concat[axis = 1](%onnx::Concat_296, %onnx::Concat_297)
      %input.183 = BatchNormalization[epsilon = 0.00100000004749745, momentum = 0.990000009536743](%input.179, %model.9.bn.weight, %model.9.bn.bias, %model.9.bn.running_mean, %model.9.bn.running_var)
      %onnx::Conv_300 = LeakyRelu[alpha = 0.100000001490116](%input.183)
      %input.187 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_300, %model.9.cv4.conv.weight, %model.9.cv4.conv.bias)
      %onnx::Conv_302 = LeakyRelu[alpha = 0.100000001490116](%input.187)
      %input.191 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_302, %model.10.conv.weight, %model.10.conv.bias)
      %onnx::Resize_304 = LeakyRelu[alpha = 0.100000001490116](%input.191)
      %onnx::Resize_308 = Constant[value = <Tensor>]()
      %onnx::Concat_309 = Resize[coordinate_transformation_mode = 'asymmetric', cubic_coeff_a = -0.75, mode = 'nearest', nearest_mode = 'floor'](%onnx::Resize_304, %onnx::Resize_308, %onnx::Resize_419)
      %input.195 = Concat[axis = 1](%onnx::Concat_309, %onnx::Conv_279)
      %input.199 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%input.195, %model.13.cv1.conv.weight, %model.13.cv1.conv.bias)
      %onnx::Conv_312 = LeakyRelu[alpha = 0.100000001490116](%input.199)
      %input.203 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_312, %model.13.m.0.cv1.conv.weight, %model.13.m.0.cv1.conv.bias)
      %onnx::Conv_314 = LeakyRelu[alpha = 0.100000001490116](%input.203)
      %input.207 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [1, 1]](%onnx::Conv_314, %model.13.m.0.cv2.conv.weight, %model.13.m.0.cv2.conv.bias)
      %onnx::Conv_316 = LeakyRelu[alpha = 0.100000001490116](%input.207)
      %onnx::Concat_317 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_316, %model.13.cv3.weight)
      %onnx::Concat_318 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%input.195, %model.13.cv2.weight)
      %input.211 = Concat[axis = 1](%onnx::Concat_317, %onnx::Concat_318)
      %input.215 = BatchNormalization[epsilon = 0.00100000004749745, momentum = 0.990000009536743](%input.211, %model.13.bn.weight, %model.13.bn.bias, %model.13.bn.running_mean, %model.13.bn.running_var)
      %onnx::Conv_321 = LeakyRelu[alpha = 0.100000001490116](%input.215)
      %input.219 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_321, %model.13.cv4.conv.weight, %model.13.cv4.conv.bias)
      %onnx::Conv_323 = LeakyRelu[alpha = 0.100000001490116](%input.219)
      %input.223 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_323, %model.14.conv.weight, %model.14.conv.bias)
      %onnx::Resize_325 = LeakyRelu[alpha = 0.100000001490116](%input.223)
      %onnx::Resize_329 = Constant[value = <Tensor>]()
      %onnx::Concat_330 = Resize[coordinate_transformation_mode = 'asymmetric', cubic_coeff_a = -0.75, mode = 'nearest', nearest_mode = 'floor'](%onnx::Resize_325, %onnx::Resize_329, %onnx::Resize_420)
      %input.227 = Concat[axis = 1](%onnx::Concat_330, %onnx::Conv_253)
      %input.231 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%input.227, %model.17.cv1.conv.weight, %model.17.cv1.conv.bias)
      %onnx::Conv_333 = LeakyRelu[alpha = 0.100000001490116](%input.231)
      %input.235 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_333, %model.17.m.0.cv1.conv.weight, %model.17.m.0.cv1.conv.bias)
      %onnx::Conv_335 = LeakyRelu[alpha = 0.100000001490116](%input.235)
      %input.239 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [1, 1]](%onnx::Conv_335, %model.17.m.0.cv2.conv.weight, %model.17.m.0.cv2.conv.bias)
      %onnx::Conv_337 = LeakyRelu[alpha = 0.100000001490116](%input.239)
      %onnx::Concat_338 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_337, %model.17.cv3.weight)
      %onnx::Concat_339 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%input.227, %model.17.cv2.weight)
      %input.243 = Concat[axis = 1](%onnx::Concat_338, %onnx::Concat_339)
      %input.247 = BatchNormalization[epsilon = 0.00100000004749745, momentum = 0.990000009536743](%input.243, %model.17.bn.weight, %model.17.bn.bias, %model.17.bn.running_mean, %model.17.bn.running_var)
      %onnx::Conv_342 = LeakyRelu[alpha = 0.100000001490116](%input.247)
      %input.251 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_342, %model.17.cv4.conv.weight, %model.17.cv4.conv.bias)
      %onnx::Conv_344 = LeakyRelu[alpha = 0.100000001490116](%input.251)
      %input.255 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [2, 2]](%onnx::Conv_344, %model.18.conv.weight, %model.18.conv.bias)
      %onnx::Concat_346 = LeakyRelu[alpha = 0.100000001490116](%input.255)
      %input.259 = Concat[axis = 1](%onnx::Concat_346, %onnx::Resize_325)
      %input.263 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%input.259, %model.20.cv1.conv.weight, %model.20.cv1.conv.bias)
      %onnx::Conv_349 = LeakyRelu[alpha = 0.100000001490116](%input.263)
      %input.267 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_349, %model.20.m.0.cv1.conv.weight, %model.20.m.0.cv1.conv.bias)
      %onnx::Conv_351 = LeakyRelu[alpha = 0.100000001490116](%input.267)
      %input.271 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [1, 1]](%onnx::Conv_351, %model.20.m.0.cv2.conv.weight, %model.20.m.0.cv2.conv.bias)
      %onnx::Conv_353 = LeakyRelu[alpha = 0.100000001490116](%input.271)
      %onnx::Concat_354 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_353, %model.20.cv3.weight)
      %onnx::Concat_355 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%input.259, %model.20.cv2.weight)
      %input.275 = Concat[axis = 1](%onnx::Concat_354, %onnx::Concat_355)
      %input.279 = BatchNormalization[epsilon = 0.00100000004749745, momentum = 0.990000009536743](%input.275, %model.20.bn.weight, %model.20.bn.bias, %model.20.bn.running_mean, %model.20.bn.running_var)
      %onnx::Conv_358 = LeakyRelu[alpha = 0.100000001490116](%input.279)
      %input.283 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_358, %model.20.cv4.conv.weight, %model.20.cv4.conv.bias)
      %onnx::Conv_360 = LeakyRelu[alpha = 0.100000001490116](%input.283)
      %input.287 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [2, 2]](%onnx::Conv_360, %model.21.conv.weight, %model.21.conv.bias)
      %onnx::Concat_362 = LeakyRelu[alpha = 0.100000001490116](%input.287)
      %input.291 = Concat[axis = 1](%onnx::Concat_362, %onnx::Resize_304)
      %input.295 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%input.291, %model.23.cv1.conv.weight, %model.23.cv1.conv.bias)
      %onnx::Conv_365 = LeakyRelu[alpha = 0.100000001490116](%input.295)
      %input.299 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_365, %model.23.m.0.cv1.conv.weight, %model.23.m.0.cv1.conv.bias)
      %onnx::Conv_367 = LeakyRelu[alpha = 0.100000001490116](%input.299)
      %input.303 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [1, 1]](%onnx::Conv_367, %model.23.m.0.cv2.conv.weight, %model.23.m.0.cv2.conv.bias)
      %onnx::Conv_369 = LeakyRelu[alpha = 0.100000001490116](%input.303)
      %onnx::Concat_370 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_369, %model.23.cv3.weight)
      %onnx::Concat_371 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%input.291, %model.23.cv2.weight)
      %input.307 = Concat[axis = 1](%onnx::Concat_370, %onnx::Concat_371)
      %input.311 = BatchNormalization[epsilon = 0.00100000004749745, momentum = 0.990000009536743](%input.307, %model.23.bn.weight, %model.23.bn.bias, %model.23.bn.running_mean, %model.23.bn.running_var)
      %onnx::Conv_374 = LeakyRelu[alpha = 0.100000001490116](%input.311)
      %input.315 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_374, %model.23.cv4.conv.weight, %model.23.cv4.conv.bias)
      %onnx::Conv_376 = LeakyRelu[alpha = 0.100000001490116](%input.315)
      %onnx::Reshape_377 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_344, %model.24.m.0.weight, %model.24.m.0.bias)
      %onnx::Transpose_389 = Reshape(%onnx::Reshape_377, %onnx::Reshape_426)
      %output = Transpose[perm = [0, 1, 3, 4, 2]](%onnx::Transpose_389)
      %onnx::Reshape_391 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_360, %model.24.m.1.weight, %model.24.m.1.bias)
      %onnx::Transpose_403 = Reshape(%onnx::Reshape_391, %onnx::Reshape_432)
      %404 = Transpose[perm = [0, 1, 3, 4, 2]](%onnx::Transpose_403)
      %onnx::Reshape_405 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_376, %model.24.m.2.weight, %model.24.m.2.bias)
      %onnx::Transpose_417 = Reshape(%onnx::Reshape_405, %onnx::Reshape_438)
      %418 = Transpose[perm = [0, 1, 3, 4, 2]](%onnx::Transpose_417)
      return %output, %404, %418
    }
    ONNX export success, saved as ./weights/yolov5s.onnx
    CoreML export failure: No module named 'coremltools'
    ```
    

- 修改yolo.py
    
    ```bash
    Namespace(batch_size=1, img_size=[672, 672], weights='./weights/yolov5s.pt')
    
    Starting TorchScript export with torch 1.12.1+cu116...
    /home/dzp/.local/lib/python3.8/site-packages/torch/jit/_trace.py:967: TracerWarning: Encountering a list at the output of the tracer might cause the trace to be incorrect, this is only valid if the container structure does not change based on the module's inputs. Consider using a constant container instead (e.g. for `list`, use a `tuple` instead. for `dict`, use a `NamedTuple` instead). If you absolutely need this and know the side effects, pass strict=False to trace() to allow this behavior.
      module._c._create_method_from_trace(
    TorchScript export success, saved as ./weights/yolov5s.torchscript.pt
    
    Starting ONNX export with onnx 1.12.0...
    Fusing layers... Model Summary: 140 layers, 7.45958e+06 parameters, 6.61683e+06 gradients, 17.4 GFLOPS
    /home/dzp/yolov5/models/yolo.py:84: TracerWarning: Converting a tensor to a Python boolean might cause the trace to be incorrect. We can't record the data flow of Python values, so this value will be treated as a constant in the future. This means that the trace might not generalize to other inputs!
      if augment:
    /home/dzp/yolov5/models/yolo.py:108: TracerWarning: Converting a tensor to a Python boolean might cause the trace to be incorrect. We can't record the data flow of Python values, so this value will be treated as a constant in the future. This means that the trace might not generalize to other inputs!
      if profile:
    /home/dzp/yolov5/models/yolo.py:123: TracerWarning: Converting a tensor to a Python boolean might cause the trace to be incorrect. We can't record the data flow of Python values, so this value will be treated as a constant in the future. This means that the trace might not generalize to other inputs!
      if profile:
    graph torch_jit (
      %data[FLOAT, 1x3x672x672]
    ) initializers (
      %model.0.conv.conv.weight[FLOAT, 32x12x3x3]
      %model.0.conv.conv.bias[FLOAT, 32]
      %model.1.conv.weight[FLOAT, 64x32x3x3]
      %model.1.conv.bias[FLOAT, 64]
      %model.2.cv1.conv.weight[FLOAT, 32x64x1x1]
      %model.2.cv1.conv.bias[FLOAT, 32]
      %model.2.cv2.weight[FLOAT, 32x64x1x1]
      %model.2.cv3.weight[FLOAT, 32x32x1x1]
      %model.2.cv4.conv.weight[FLOAT, 64x64x1x1]
      %model.2.cv4.conv.bias[FLOAT, 64]
      %model.2.bn.weight[FLOAT, 64]
      %model.2.bn.bias[FLOAT, 64]
      %model.2.bn.running_mean[FLOAT, 64]
      %model.2.bn.running_var[FLOAT, 64]
      %model.2.m.0.cv1.conv.weight[FLOAT, 32x32x1x1]
      %model.2.m.0.cv1.conv.bias[FLOAT, 32]
      %model.2.m.0.cv2.conv.weight[FLOAT, 32x32x3x3]
      %model.2.m.0.cv2.conv.bias[FLOAT, 32]
      %model.3.conv.weight[FLOAT, 128x64x3x3]
      %model.3.conv.bias[FLOAT, 128]
      %model.4.cv1.conv.weight[FLOAT, 64x128x1x1]
      %model.4.cv1.conv.bias[FLOAT, 64]
      %model.4.cv2.weight[FLOAT, 64x128x1x1]
      %model.4.cv3.weight[FLOAT, 64x64x1x1]
      %model.4.cv4.conv.weight[FLOAT, 128x128x1x1]
      %model.4.cv4.conv.bias[FLOAT, 128]
      %model.4.bn.weight[FLOAT, 128]
      %model.4.bn.bias[FLOAT, 128]
      %model.4.bn.running_mean[FLOAT, 128]
      %model.4.bn.running_var[FLOAT, 128]
      %model.4.m.0.cv1.conv.weight[FLOAT, 64x64x1x1]
      %model.4.m.0.cv1.conv.bias[FLOAT, 64]
      %model.4.m.0.cv2.conv.weight[FLOAT, 64x64x3x3]
      %model.4.m.0.cv2.conv.bias[FLOAT, 64]
      %model.4.m.1.cv1.conv.weight[FLOAT, 64x64x1x1]
      %model.4.m.1.cv1.conv.bias[FLOAT, 64]
      %model.4.m.1.cv2.conv.weight[FLOAT, 64x64x3x3]
      %model.4.m.1.cv2.conv.bias[FLOAT, 64]
      %model.4.m.2.cv1.conv.weight[FLOAT, 64x64x1x1]
      %model.4.m.2.cv1.conv.bias[FLOAT, 64]
      %model.4.m.2.cv2.conv.weight[FLOAT, 64x64x3x3]
      %model.4.m.2.cv2.conv.bias[FLOAT, 64]
      %model.5.conv.weight[FLOAT, 256x128x3x3]
      %model.5.conv.bias[FLOAT, 256]
      %model.6.cv1.conv.weight[FLOAT, 128x256x1x1]
      %model.6.cv1.conv.bias[FLOAT, 128]
      %model.6.cv2.weight[FLOAT, 128x256x1x1]
      %model.6.cv3.weight[FLOAT, 128x128x1x1]
      %model.6.cv4.conv.weight[FLOAT, 256x256x1x1]
      %model.6.cv4.conv.bias[FLOAT, 256]
      %model.6.bn.weight[FLOAT, 256]
      %model.6.bn.bias[FLOAT, 256]
      %model.6.bn.running_mean[FLOAT, 256]
      %model.6.bn.running_var[FLOAT, 256]
      %model.6.m.0.cv1.conv.weight[FLOAT, 128x128x1x1]
      %model.6.m.0.cv1.conv.bias[FLOAT, 128]
      %model.6.m.0.cv2.conv.weight[FLOAT, 128x128x3x3]
      %model.6.m.0.cv2.conv.bias[FLOAT, 128]
      %model.6.m.1.cv1.conv.weight[FLOAT, 128x128x1x1]
      %model.6.m.1.cv1.conv.bias[FLOAT, 128]
      %model.6.m.1.cv2.conv.weight[FLOAT, 128x128x3x3]
      %model.6.m.1.cv2.conv.bias[FLOAT, 128]
      %model.6.m.2.cv1.conv.weight[FLOAT, 128x128x1x1]
      %model.6.m.2.cv1.conv.bias[FLOAT, 128]
      %model.6.m.2.cv2.conv.weight[FLOAT, 128x128x3x3]
      %model.6.m.2.cv2.conv.bias[FLOAT, 128]
      %model.7.conv.weight[FLOAT, 512x256x3x3]
      %model.7.conv.bias[FLOAT, 512]
      %model.8.cv1.conv.weight[FLOAT, 256x512x1x1]
      %model.8.cv1.conv.bias[FLOAT, 256]
      %model.8.cv2.conv.weight[FLOAT, 512x1024x1x1]
      %model.8.cv2.conv.bias[FLOAT, 512]
      %model.9.cv1.conv.weight[FLOAT, 256x512x1x1]
      %model.9.cv1.conv.bias[FLOAT, 256]
      %model.9.cv2.weight[FLOAT, 256x512x1x1]
      %model.9.cv3.weight[FLOAT, 256x256x1x1]
      %model.9.cv4.conv.weight[FLOAT, 512x512x1x1]
      %model.9.cv4.conv.bias[FLOAT, 512]
      %model.9.bn.weight[FLOAT, 512]
      %model.9.bn.bias[FLOAT, 512]
      %model.9.bn.running_mean[FLOAT, 512]
      %model.9.bn.running_var[FLOAT, 512]
      %model.9.m.0.cv1.conv.weight[FLOAT, 256x256x1x1]
      %model.9.m.0.cv1.conv.bias[FLOAT, 256]
      %model.9.m.0.cv2.conv.weight[FLOAT, 256x256x3x3]
      %model.9.m.0.cv2.conv.bias[FLOAT, 256]
      %model.10.conv.weight[FLOAT, 256x512x1x1]
      %model.10.conv.bias[FLOAT, 256]
      %model.13.cv1.conv.weight[FLOAT, 128x512x1x1]
      %model.13.cv1.conv.bias[FLOAT, 128]
      %model.13.cv2.weight[FLOAT, 128x512x1x1]
      %model.13.cv3.weight[FLOAT, 128x128x1x1]
      %model.13.cv4.conv.weight[FLOAT, 256x256x1x1]
      %model.13.cv4.conv.bias[FLOAT, 256]
      %model.13.bn.weight[FLOAT, 256]
      %model.13.bn.bias[FLOAT, 256]
      %model.13.bn.running_mean[FLOAT, 256]
      %model.13.bn.running_var[FLOAT, 256]
      %model.13.m.0.cv1.conv.weight[FLOAT, 128x128x1x1]
      %model.13.m.0.cv1.conv.bias[FLOAT, 128]
      %model.13.m.0.cv2.conv.weight[FLOAT, 128x128x3x3]
      %model.13.m.0.cv2.conv.bias[FLOAT, 128]
      %model.14.conv.weight[FLOAT, 128x256x1x1]
      %model.14.conv.bias[FLOAT, 128]
      %model.17.cv1.conv.weight[FLOAT, 64x256x1x1]
      %model.17.cv1.conv.bias[FLOAT, 64]
      %model.17.cv2.weight[FLOAT, 64x256x1x1]
      %model.17.cv3.weight[FLOAT, 64x64x1x1]
      %model.17.cv4.conv.weight[FLOAT, 128x128x1x1]
      %model.17.cv4.conv.bias[FLOAT, 128]
      %model.17.bn.weight[FLOAT, 128]
      %model.17.bn.bias[FLOAT, 128]
      %model.17.bn.running_mean[FLOAT, 128]
      %model.17.bn.running_var[FLOAT, 128]
      %model.17.m.0.cv1.conv.weight[FLOAT, 64x64x1x1]
      %model.17.m.0.cv1.conv.bias[FLOAT, 64]
      %model.17.m.0.cv2.conv.weight[FLOAT, 64x64x3x3]
      %model.17.m.0.cv2.conv.bias[FLOAT, 64]
      %model.18.conv.weight[FLOAT, 128x128x3x3]
      %model.18.conv.bias[FLOAT, 128]
      %model.20.cv1.conv.weight[FLOAT, 128x256x1x1]
      %model.20.cv1.conv.bias[FLOAT, 128]
      %model.20.cv2.weight[FLOAT, 128x256x1x1]
      %model.20.cv3.weight[FLOAT, 128x128x1x1]
      %model.20.cv4.conv.weight[FLOAT, 256x256x1x1]
      %model.20.cv4.conv.bias[FLOAT, 256]
      %model.20.bn.weight[FLOAT, 256]
      %model.20.bn.bias[FLOAT, 256]
      %model.20.bn.running_mean[FLOAT, 256]
      %model.20.bn.running_var[FLOAT, 256]
      %model.20.m.0.cv1.conv.weight[FLOAT, 128x128x1x1]
      %model.20.m.0.cv1.conv.bias[FLOAT, 128]
      %model.20.m.0.cv2.conv.weight[FLOAT, 128x128x3x3]
      %model.20.m.0.cv2.conv.bias[FLOAT, 128]
      %model.21.conv.weight[FLOAT, 256x256x3x3]
      %model.21.conv.bias[FLOAT, 256]
      %model.23.cv1.conv.weight[FLOAT, 256x512x1x1]
      %model.23.cv1.conv.bias[FLOAT, 256]
      %model.23.cv2.weight[FLOAT, 256x512x1x1]
      %model.23.cv3.weight[FLOAT, 256x256x1x1]
      %model.23.cv4.conv.weight[FLOAT, 512x512x1x1]
      %model.23.cv4.conv.bias[FLOAT, 512]
      %model.23.bn.weight[FLOAT, 512]
      %model.23.bn.bias[FLOAT, 512]
      %model.23.bn.running_mean[FLOAT, 512]
      %model.23.bn.running_var[FLOAT, 512]
      %model.23.m.0.cv1.conv.weight[FLOAT, 256x256x1x1]
      %model.23.m.0.cv1.conv.bias[FLOAT, 256]
      %model.23.m.0.cv2.conv.weight[FLOAT, 256x256x3x3]
      %model.23.m.0.cv2.conv.bias[FLOAT, 256]
      %model.24.m.0.weight[FLOAT, 255x128x1x1]
      %model.24.m.0.bias[FLOAT, 255]
      %model.24.m.1.weight[FLOAT, 255x256x1x1]
      %model.24.m.1.bias[FLOAT, 255]
      %model.24.m.2.weight[FLOAT, 255x512x1x1]
      %model.24.m.2.bias[FLOAT, 255]
      %onnx::Resize_383[FLOAT, 4]
    ) {
      %onnx::Resize_384 = Identity(%onnx::Resize_383)
      %onnx::Slice_169 = Constant[value = <Tensor>]()
      %onnx::Slice_170 = Constant[value = <Tensor>]()
      %onnx::Slice_171 = Constant[value = <Tensor>]()
      %onnx::Slice_172 = Constant[value = <Tensor>]()
      %onnx::Slice_173 = Slice(%data, %onnx::Slice_170, %onnx::Slice_171, %onnx::Slice_169, %onnx::Slice_172)
      %onnx::Slice_174 = Constant[value = <Tensor>]()
      %onnx::Slice_175 = Constant[value = <Tensor>]()
      %onnx::Slice_176 = Constant[value = <Tensor>]()
      %onnx::Slice_177 = Constant[value = <Tensor>]()
      %onnx::Concat_178 = Slice(%onnx::Slice_173, %onnx::Slice_175, %onnx::Slice_176, %onnx::Slice_174, %onnx::Slice_177)
      %onnx::Slice_179 = Constant[value = <Tensor>]()
      %onnx::Slice_180 = Constant[value = <Tensor>]()
      %onnx::Slice_181 = Constant[value = <Tensor>]()
      %onnx::Slice_182 = Constant[value = <Tensor>]()
      %onnx::Slice_183 = Slice(%data, %onnx::Slice_180, %onnx::Slice_181, %onnx::Slice_179, %onnx::Slice_182)
      %onnx::Slice_184 = Constant[value = <Tensor>]()
      %onnx::Slice_185 = Constant[value = <Tensor>]()
      %onnx::Slice_186 = Constant[value = <Tensor>]()
      %onnx::Slice_187 = Constant[value = <Tensor>]()
      %onnx::Concat_188 = Slice(%onnx::Slice_183, %onnx::Slice_185, %onnx::Slice_186, %onnx::Slice_184, %onnx::Slice_187)
      %onnx::Slice_189 = Constant[value = <Tensor>]()
      %onnx::Slice_190 = Constant[value = <Tensor>]()
      %onnx::Slice_191 = Constant[value = <Tensor>]()
      %onnx::Slice_192 = Constant[value = <Tensor>]()
      %onnx::Slice_193 = Slice(%data, %onnx::Slice_190, %onnx::Slice_191, %onnx::Slice_189, %onnx::Slice_192)
      %onnx::Slice_194 = Constant[value = <Tensor>]()
      %onnx::Slice_195 = Constant[value = <Tensor>]()
      %onnx::Slice_196 = Constant[value = <Tensor>]()
      %onnx::Slice_197 = Constant[value = <Tensor>]()
      %onnx::Concat_198 = Slice(%onnx::Slice_193, %onnx::Slice_195, %onnx::Slice_196, %onnx::Slice_194, %onnx::Slice_197)
      %onnx::Slice_199 = Constant[value = <Tensor>]()
      %onnx::Slice_200 = Constant[value = <Tensor>]()
      %onnx::Slice_201 = Constant[value = <Tensor>]()
      %onnx::Slice_202 = Constant[value = <Tensor>]()
      %onnx::Slice_203 = Slice(%data, %onnx::Slice_200, %onnx::Slice_201, %onnx::Slice_199, %onnx::Slice_202)
      %onnx::Slice_204 = Constant[value = <Tensor>]()
      %onnx::Slice_205 = Constant[value = <Tensor>]()
      %onnx::Slice_206 = Constant[value = <Tensor>]()
      %onnx::Slice_207 = Constant[value = <Tensor>]()
      %onnx::Concat_208 = Slice(%onnx::Slice_203, %onnx::Slice_205, %onnx::Slice_206, %onnx::Slice_204, %onnx::Slice_207)
      %input = Concat[axis = 1](%onnx::Concat_178, %onnx::Concat_188, %onnx::Concat_198, %onnx::Concat_208)
      %input.3 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [1, 1]](%input, %model.0.conv.conv.weight, %model.0.conv.conv.bias)
      %onnx::Conv_211 = LeakyRelu[alpha = 0.100000001490116](%input.3)
      %input.7 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [2, 2]](%onnx::Conv_211, %model.1.conv.weight, %model.1.conv.bias)
      %onnx::Conv_213 = LeakyRelu[alpha = 0.100000001490116](%input.7)
      %input.11 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_213, %model.2.cv1.conv.weight, %model.2.cv1.conv.bias)
      %onnx::Conv_215 = LeakyRelu[alpha = 0.100000001490116](%input.11)
      %input.15 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_215, %model.2.m.0.cv1.conv.weight, %model.2.m.0.cv1.conv.bias)
      %onnx::Conv_217 = LeakyRelu[alpha = 0.100000001490116](%input.15)
      %input.19 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [1, 1]](%onnx::Conv_217, %model.2.m.0.cv2.conv.weight, %model.2.m.0.cv2.conv.bias)
      %onnx::Add_219 = LeakyRelu[alpha = 0.100000001490116](%input.19)
      %input.23 = Add(%onnx::Conv_215, %onnx::Add_219)
      %onnx::Concat_221 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%input.23, %model.2.cv3.weight)
      %onnx::Concat_222 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_213, %model.2.cv2.weight)
      %input.27 = Concat[axis = 1](%onnx::Concat_221, %onnx::Concat_222)
      %input.31 = BatchNormalization[epsilon = 0.00100000004749745, momentum = 0.990000009536743](%input.27, %model.2.bn.weight, %model.2.bn.bias, %model.2.bn.running_mean, %model.2.bn.running_var)
      %onnx::Conv_225 = LeakyRelu[alpha = 0.100000001490116](%input.31)
      %input.35 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_225, %model.2.cv4.conv.weight, %model.2.cv4.conv.bias)
      %onnx::Conv_227 = LeakyRelu[alpha = 0.100000001490116](%input.35)
      %input.39 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [2, 2]](%onnx::Conv_227, %model.3.conv.weight, %model.3.conv.bias)
      %onnx::Conv_229 = LeakyRelu[alpha = 0.100000001490116](%input.39)
      %input.43 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_229, %model.4.cv1.conv.weight, %model.4.cv1.conv.bias)
      %onnx::Conv_231 = LeakyRelu[alpha = 0.100000001490116](%input.43)
      %input.47 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_231, %model.4.m.0.cv1.conv.weight, %model.4.m.0.cv1.conv.bias)
      %onnx::Conv_233 = LeakyRelu[alpha = 0.100000001490116](%input.47)
      %input.51 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [1, 1]](%onnx::Conv_233, %model.4.m.0.cv2.conv.weight, %model.4.m.0.cv2.conv.bias)
      %onnx::Add_235 = LeakyRelu[alpha = 0.100000001490116](%input.51)
      %input.55 = Add(%onnx::Conv_231, %onnx::Add_235)
      %input.59 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%input.55, %model.4.m.1.cv1.conv.weight, %model.4.m.1.cv1.conv.bias)
      %onnx::Conv_238 = LeakyRelu[alpha = 0.100000001490116](%input.59)
      %input.63 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [1, 1]](%onnx::Conv_238, %model.4.m.1.cv2.conv.weight, %model.4.m.1.cv2.conv.bias)
      %onnx::Add_240 = LeakyRelu[alpha = 0.100000001490116](%input.63)
      %input.67 = Add(%input.55, %onnx::Add_240)
      %input.71 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%input.67, %model.4.m.2.cv1.conv.weight, %model.4.m.2.cv1.conv.bias)
      %onnx::Conv_243 = LeakyRelu[alpha = 0.100000001490116](%input.71)
      %input.75 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [1, 1]](%onnx::Conv_243, %model.4.m.2.cv2.conv.weight, %model.4.m.2.cv2.conv.bias)
      %onnx::Add_245 = LeakyRelu[alpha = 0.100000001490116](%input.75)
      %input.79 = Add(%input.67, %onnx::Add_245)
      %onnx::Concat_247 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%input.79, %model.4.cv3.weight)
      %onnx::Concat_248 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_229, %model.4.cv2.weight)
      %input.83 = Concat[axis = 1](%onnx::Concat_247, %onnx::Concat_248)
      %input.87 = BatchNormalization[epsilon = 0.00100000004749745, momentum = 0.990000009536743](%input.83, %model.4.bn.weight, %model.4.bn.bias, %model.4.bn.running_mean, %model.4.bn.running_var)
      %onnx::Conv_251 = LeakyRelu[alpha = 0.100000001490116](%input.87)
      %input.91 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_251, %model.4.cv4.conv.weight, %model.4.cv4.conv.bias)
      %onnx::Conv_253 = LeakyRelu[alpha = 0.100000001490116](%input.91)
      %input.95 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [2, 2]](%onnx::Conv_253, %model.5.conv.weight, %model.5.conv.bias)
      %onnx::Conv_255 = LeakyRelu[alpha = 0.100000001490116](%input.95)
      %input.99 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_255, %model.6.cv1.conv.weight, %model.6.cv1.conv.bias)
      %onnx::Conv_257 = LeakyRelu[alpha = 0.100000001490116](%input.99)
      %input.103 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_257, %model.6.m.0.cv1.conv.weight, %model.6.m.0.cv1.conv.bias)
      %onnx::Conv_259 = LeakyRelu[alpha = 0.100000001490116](%input.103)
      %input.107 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [1, 1]](%onnx::Conv_259, %model.6.m.0.cv2.conv.weight, %model.6.m.0.cv2.conv.bias)
      %onnx::Add_261 = LeakyRelu[alpha = 0.100000001490116](%input.107)
      %input.111 = Add(%onnx::Conv_257, %onnx::Add_261)
      %input.115 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%input.111, %model.6.m.1.cv1.conv.weight, %model.6.m.1.cv1.conv.bias)
      %onnx::Conv_264 = LeakyRelu[alpha = 0.100000001490116](%input.115)
      %input.119 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [1, 1]](%onnx::Conv_264, %model.6.m.1.cv2.conv.weight, %model.6.m.1.cv2.conv.bias)
      %onnx::Add_266 = LeakyRelu[alpha = 0.100000001490116](%input.119)
      %input.123 = Add(%input.111, %onnx::Add_266)
      %input.127 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%input.123, %model.6.m.2.cv1.conv.weight, %model.6.m.2.cv1.conv.bias)
      %onnx::Conv_269 = LeakyRelu[alpha = 0.100000001490116](%input.127)
      %input.131 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [1, 1]](%onnx::Conv_269, %model.6.m.2.cv2.conv.weight, %model.6.m.2.cv2.conv.bias)
      %onnx::Add_271 = LeakyRelu[alpha = 0.100000001490116](%input.131)
      %input.135 = Add(%input.123, %onnx::Add_271)
      %onnx::Concat_273 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%input.135, %model.6.cv3.weight)
      %onnx::Concat_274 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_255, %model.6.cv2.weight)
      %input.139 = Concat[axis = 1](%onnx::Concat_273, %onnx::Concat_274)
      %input.143 = BatchNormalization[epsilon = 0.00100000004749745, momentum = 0.990000009536743](%input.139, %model.6.bn.weight, %model.6.bn.bias, %model.6.bn.running_mean, %model.6.bn.running_var)
      %onnx::Conv_277 = LeakyRelu[alpha = 0.100000001490116](%input.143)
      %input.147 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_277, %model.6.cv4.conv.weight, %model.6.cv4.conv.bias)
      %onnx::Conv_279 = LeakyRelu[alpha = 0.100000001490116](%input.147)
      %input.151 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [2, 2]](%onnx::Conv_279, %model.7.conv.weight, %model.7.conv.bias)
      %onnx::Conv_281 = LeakyRelu[alpha = 0.100000001490116](%input.151)
      %input.155 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_281, %model.8.cv1.conv.weight, %model.8.cv1.conv.bias)
      %onnx::MaxPool_283 = LeakyRelu[alpha = 0.100000001490116](%input.155)
      %onnx::Concat_284 = MaxPool[ceil_mode = 0, kernel_shape = [5, 5], pads = [2, 2, 2, 2], strides = [1, 1]](%onnx::MaxPool_283)
      %onnx::Concat_285 = MaxPool[ceil_mode = 0, kernel_shape = [9, 9], pads = [4, 4, 4, 4], strides = [1, 1]](%onnx::MaxPool_283)
      %onnx::Concat_286 = MaxPool[ceil_mode = 0, kernel_shape = [13, 13], pads = [6, 6, 6, 6], strides = [1, 1]](%onnx::MaxPool_283)
      %input.159 = Concat[axis = 1](%onnx::MaxPool_283, %onnx::Concat_284, %onnx::Concat_285, %onnx::Concat_286)
      %input.163 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%input.159, %model.8.cv2.conv.weight, %model.8.cv2.conv.bias)
      %onnx::Conv_289 = LeakyRelu[alpha = 0.100000001490116](%input.163)
      %input.167 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_289, %model.9.cv1.conv.weight, %model.9.cv1.conv.bias)
      %onnx::Conv_291 = LeakyRelu[alpha = 0.100000001490116](%input.167)
      %input.171 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_291, %model.9.m.0.cv1.conv.weight, %model.9.m.0.cv1.conv.bias)
      %onnx::Conv_293 = LeakyRelu[alpha = 0.100000001490116](%input.171)
      %input.175 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [1, 1]](%onnx::Conv_293, %model.9.m.0.cv2.conv.weight, %model.9.m.0.cv2.conv.bias)
      %onnx::Conv_295 = LeakyRelu[alpha = 0.100000001490116](%input.175)
      %onnx::Concat_296 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_295, %model.9.cv3.weight)
      %onnx::Concat_297 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_289, %model.9.cv2.weight)
      %input.179 = Concat[axis = 1](%onnx::Concat_296, %onnx::Concat_297)
      %input.183 = BatchNormalization[epsilon = 0.00100000004749745, momentum = 0.990000009536743](%input.179, %model.9.bn.weight, %model.9.bn.bias, %model.9.bn.running_mean, %model.9.bn.running_var)
      %onnx::Conv_300 = LeakyRelu[alpha = 0.100000001490116](%input.183)
      %input.187 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_300, %model.9.cv4.conv.weight, %model.9.cv4.conv.bias)
      %onnx::Conv_302 = LeakyRelu[alpha = 0.100000001490116](%input.187)
      %input.191 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_302, %model.10.conv.weight, %model.10.conv.bias)
      %onnx::Resize_304 = LeakyRelu[alpha = 0.100000001490116](%input.191)
      %onnx::Resize_308 = Constant[value = <Tensor>]()
      %onnx::Concat_309 = Resize[coordinate_transformation_mode = 'asymmetric', cubic_coeff_a = -0.75, mode = 'nearest', nearest_mode = 'floor'](%onnx::Resize_304, %onnx::Resize_308, %onnx::Resize_383)
      %input.195 = Concat[axis = 1](%onnx::Concat_309, %onnx::Conv_279)
      %input.199 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%input.195, %model.13.cv1.conv.weight, %model.13.cv1.conv.bias)
      %onnx::Conv_312 = LeakyRelu[alpha = 0.100000001490116](%input.199)
      %input.203 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_312, %model.13.m.0.cv1.conv.weight, %model.13.m.0.cv1.conv.bias)
      %onnx::Conv_314 = LeakyRelu[alpha = 0.100000001490116](%input.203)
      %input.207 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [1, 1]](%onnx::Conv_314, %model.13.m.0.cv2.conv.weight, %model.13.m.0.cv2.conv.bias)
      %onnx::Conv_316 = LeakyRelu[alpha = 0.100000001490116](%input.207)
      %onnx::Concat_317 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_316, %model.13.cv3.weight)
      %onnx::Concat_318 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%input.195, %model.13.cv2.weight)
      %input.211 = Concat[axis = 1](%onnx::Concat_317, %onnx::Concat_318)
      %input.215 = BatchNormalization[epsilon = 0.00100000004749745, momentum = 0.990000009536743](%input.211, %model.13.bn.weight, %model.13.bn.bias, %model.13.bn.running_mean, %model.13.bn.running_var)
      %onnx::Conv_321 = LeakyRelu[alpha = 0.100000001490116](%input.215)
      %input.219 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_321, %model.13.cv4.conv.weight, %model.13.cv4.conv.bias)
      %onnx::Conv_323 = LeakyRelu[alpha = 0.100000001490116](%input.219)
      %input.223 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_323, %model.14.conv.weight, %model.14.conv.bias)
      %onnx::Resize_325 = LeakyRelu[alpha = 0.100000001490116](%input.223)
      %onnx::Resize_329 = Constant[value = <Tensor>]()
      %onnx::Concat_330 = Resize[coordinate_transformation_mode = 'asymmetric', cubic_coeff_a = -0.75, mode = 'nearest', nearest_mode = 'floor'](%onnx::Resize_325, %onnx::Resize_329, %onnx::Resize_384)
      %input.227 = Concat[axis = 1](%onnx::Concat_330, %onnx::Conv_253)
      %input.231 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%input.227, %model.17.cv1.conv.weight, %model.17.cv1.conv.bias)
      %onnx::Conv_333 = LeakyRelu[alpha = 0.100000001490116](%input.231)
      %input.235 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_333, %model.17.m.0.cv1.conv.weight, %model.17.m.0.cv1.conv.bias)
      %onnx::Conv_335 = LeakyRelu[alpha = 0.100000001490116](%input.235)
      %input.239 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [1, 1]](%onnx::Conv_335, %model.17.m.0.cv2.conv.weight, %model.17.m.0.cv2.conv.bias)
      %onnx::Conv_337 = LeakyRelu[alpha = 0.100000001490116](%input.239)
      %onnx::Concat_338 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_337, %model.17.cv3.weight)
      %onnx::Concat_339 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%input.227, %model.17.cv2.weight)
      %input.243 = Concat[axis = 1](%onnx::Concat_338, %onnx::Concat_339)
      %input.247 = BatchNormalization[epsilon = 0.00100000004749745, momentum = 0.990000009536743](%input.243, %model.17.bn.weight, %model.17.bn.bias, %model.17.bn.running_mean, %model.17.bn.running_var)
      %onnx::Conv_342 = LeakyRelu[alpha = 0.100000001490116](%input.247)
      %input.251 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_342, %model.17.cv4.conv.weight, %model.17.cv4.conv.bias)
      %onnx::Conv_344 = LeakyRelu[alpha = 0.100000001490116](%input.251)
      %input.255 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [2, 2]](%onnx::Conv_344, %model.18.conv.weight, %model.18.conv.bias)
      %onnx::Concat_346 = LeakyRelu[alpha = 0.100000001490116](%input.255)
      %input.259 = Concat[axis = 1](%onnx::Concat_346, %onnx::Resize_325)
      %input.263 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%input.259, %model.20.cv1.conv.weight, %model.20.cv1.conv.bias)
      %onnx::Conv_349 = LeakyRelu[alpha = 0.100000001490116](%input.263)
      %input.267 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_349, %model.20.m.0.cv1.conv.weight, %model.20.m.0.cv1.conv.bias)
      %onnx::Conv_351 = LeakyRelu[alpha = 0.100000001490116](%input.267)
      %input.271 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [1, 1]](%onnx::Conv_351, %model.20.m.0.cv2.conv.weight, %model.20.m.0.cv2.conv.bias)
      %onnx::Conv_353 = LeakyRelu[alpha = 0.100000001490116](%input.271)
      %onnx::Concat_354 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_353, %model.20.cv3.weight)
      %onnx::Concat_355 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%input.259, %model.20.cv2.weight)
      %input.275 = Concat[axis = 1](%onnx::Concat_354, %onnx::Concat_355)
      %input.279 = BatchNormalization[epsilon = 0.00100000004749745, momentum = 0.990000009536743](%input.275, %model.20.bn.weight, %model.20.bn.bias, %model.20.bn.running_mean, %model.20.bn.running_var)
      %onnx::Conv_358 = LeakyRelu[alpha = 0.100000001490116](%input.279)
      %input.283 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_358, %model.20.cv4.conv.weight, %model.20.cv4.conv.bias)
      %onnx::Conv_360 = LeakyRelu[alpha = 0.100000001490116](%input.283)
      %input.287 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [2, 2]](%onnx::Conv_360, %model.21.conv.weight, %model.21.conv.bias)
      %onnx::Concat_362 = LeakyRelu[alpha = 0.100000001490116](%input.287)
      %input.291 = Concat[axis = 1](%onnx::Concat_362, %onnx::Resize_304)
      %input.295 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%input.291, %model.23.cv1.conv.weight, %model.23.cv1.conv.bias)
      %onnx::Conv_365 = LeakyRelu[alpha = 0.100000001490116](%input.295)
      %input.299 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_365, %model.23.m.0.cv1.conv.weight, %model.23.m.0.cv1.conv.bias)
      %onnx::Conv_367 = LeakyRelu[alpha = 0.100000001490116](%input.299)
      %input.303 = Conv[dilations = [1, 1], group = 1, kernel_shape = [3, 3], pads = [1, 1, 1, 1], strides = [1, 1]](%onnx::Conv_367, %model.23.m.0.cv2.conv.weight, %model.23.m.0.cv2.conv.bias)
      %onnx::Conv_369 = LeakyRelu[alpha = 0.100000001490116](%input.303)
      %onnx::Concat_370 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_369, %model.23.cv3.weight)
      %onnx::Concat_371 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%input.291, %model.23.cv2.weight)
      %input.307 = Concat[axis = 1](%onnx::Concat_370, %onnx::Concat_371)
      %input.311 = BatchNormalization[epsilon = 0.00100000004749745, momentum = 0.990000009536743](%input.307, %model.23.bn.weight, %model.23.bn.bias, %model.23.bn.running_mean, %model.23.bn.running_var)
      %onnx::Conv_374 = LeakyRelu[alpha = 0.100000001490116](%input.311)
      %input.315 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_374, %model.23.cv4.conv.weight, %model.23.cv4.conv.bias)
      %onnx::Conv_376 = LeakyRelu[alpha = 0.100000001490116](%input.315)
      %onnx::Transpose_377 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_344, %model.24.m.0.weight, %model.24.m.0.bias)
      %output = Transpose[perm = [0, 2, 3, 1]](%onnx::Transpose_377)
      %onnx::Transpose_379 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_360, %model.24.m.1.weight, %model.24.m.1.bias)
      %380 = Transpose[perm = [0, 2, 3, 1]](%onnx::Transpose_379)
      %onnx::Transpose_381 = Conv[dilations = [1, 1], group = 1, kernel_shape = [1, 1], pads = [0, 0, 0, 0], strides = [1, 1]](%onnx::Conv_376, %model.24.m.2.weight, %model.24.m.2.bias)
      %382 = Transpose[perm = [0, 2, 3, 1]](%onnx::Transpose_381)
      return %output, %380, %382
    }
    ONNX export success, saved as ./weights/yolov5s.onnx
    CoreML export failure: No module named 'coremltools'
    ```
    

### YOLOv5s ONNX结构图（最新版）

![yolov5s.onnx.svg](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/1a3753bb-b527-4fbf-bba4-95bd36f0e1e8/yolov5s.onnx.svg)

### YOLOv5s ONNX v2.0版结构图

![yolov5s.onnx (1).svg](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/eb3cf4a6-3645-4584-8396-ac12091d63fd/yolov5s.onnx_(1).svg)

<aside>
⚠️ 地平线官方文档中提到一处对yolo.py文件的修改：

```python
def forward(self, x):
    # x = x.copy()  # for profiling
    z = []  # inference output
    self.training |= self.export
    for i in range(self.nl):
        x[i] = self.m[i](x[i])  # conv
        bs, _, ny, nx = x[i].shape  # x(bs,255,20,20) to x(bs,3,20,20,85)
        #  x[i] = x[i].view(bs, self.na, self.no, ny, nx).permute(0, 1, 3, 4, 2).contiguous()
        x[i] = x[i].permute(0, 2, 3, 1).contiguous()
```

针对是否有必要做该修改，以及该修改的影响，分别进行实验。

</aside>

- 未做修改时 `bash 01_check.sh` 的输出
    
    ```bash
    cd $(dirname $0) || exit
    
    MODEL_NAME=${1:-yolov5s}
    
    model_type="onnx"
    onnx_model="./models/$MODEL_NAME.onnx"
    march="bernoulli2"
    
    hb_mapper checker --model-type ${model_type} \
                      --model ${onnx_model} \
                      --march ${march}
    /usr/local/lib/python3.6/site-packages/paramiko/transport.py:33: CryptographyDeprecationWarning: Python 3.6 is no longer supported by the Python core team. Therefore, support for it is deprecated in cryptography and will be removed in a future release.
      from cryptography.hazmat.backends import default_backend
    2023-01-10 11:03:45,663 INFO log will be stored in /open_explorer/smart_vision/hb_mapper_checker.log
    2023-01-10 11:03:45,663 INFO Start hb_mapper....
    2023-01-10 11:03:45,663 INFO hbdk version 3.41.4
    2023-01-10 11:03:45,663 INFO horizon_nn version 0.15.3
    2023-01-10 11:03:45,663 INFO hb_mapper version 1.13.3
    2023-01-10 11:03:45,681 INFO Model type: onnx
    2023-01-10 11:03:45,681 INFO input names []
    2023-01-10 11:03:45,681 INFO input shapes {}
    2023-01-10 11:03:45,681 INFO Begin model checking....
    2023-01-10 11:03:45,692 INFO [Tue Jan 10 11:03:45 2023] Start to Horizon NN Model Convert.
    2023-01-10 11:03:45,692 INFO The input parameter is not specified, convert with default parameters.
    2023-01-10 11:03:45,692 INFO Parsing the hbdk parameter:{'hbdk_pass_through_params': '--O0'}
    2023-01-10 11:03:45,692 INFO HorizonNN version: 0.15.3
    2023-01-10 11:03:45,693 INFO HBDK version: 3.41.4
    2023-01-10 11:03:45,693 INFO [Tue Jan 10 11:03:45 2023] Start to parse the onnx model.
    2023-01-10 11:03:45,708 INFO Input ONNX model infomation:
    ONNX IR version:          6
    Opset version:            [11]
    Producer:                 pytorch1.12.1
    Domain:                   none
    Input name:               data, [1, 3, 672, 672]
    Output name:              output, [1, 3, 84, 84, 85]
    Output name:              404, [1, 3, 42, 42, 85]
    Output name:              418, [1, 3, 21, 21, 85]
    2023-01-10 11:03:45,807 INFO [Tue Jan 10 11:03:45 2023] End to parse the onnx model.
    2023-01-10 11:03:45,807 INFO Model input names parsed from model: ['data']
    2023-01-10 11:03:45,821 INFO Saving the original float model: ./.hb_check/original_float_model.onnx.
    2023-01-10 11:03:45,821 INFO [Tue Jan 10 11:03:45 2023] Start to optimize the model.
    2023-01-10 11:03:46,231 INFO [Tue Jan 10 11:03:46 2023] End to optimize the model.
    2023-01-10 11:03:46,245 INFO Saving the optimized model: ./.hb_check/optimized_float_model.onnx.
    2023-01-10 11:03:46,245 INFO [Tue Jan 10 11:03:46 2023] Start to calibrate the model.
    2023-01-10 11:03:46,251 INFO There are 1 samples in the calibration data set.
    2023-01-10 11:03:46,387 INFO Run calibration model with max method.
    max calibration in progress: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  4.36it/s]
    2023-01-10 11:03:46,822 INFO [Tue Jan 10 11:03:46 2023] End to calibrate the model.
    2023-01-10 11:03:46,822 INFO [Tue Jan 10 11:03:46 2023] Start to quantize the model.
    2023-01-10 11:03:47,878 INFO [Tue Jan 10 11:03:47 2023] End to quantize the model.
    2023-01-10 11:03:48,049 INFO Saving the quantized model: ./.hb_check/quantized_model.onnx.
    2023-01-10 11:03:48,564 INFO [Tue Jan 10 11:03:48 2023] Start to compile the model with march bernoulli2.
    2023-01-10 11:03:48,807 INFO Compile submodel: torch_jit_subgraph_0
    2023-01-10 11:03:49,177 INFO hbdk-cc parameters:['--O0', '--input-layout', 'NHWC', '--output-layout', 'NCHW']
    2023-01-10 11:03:49,212 INFO INFO: "-j" or "--jobs" is not specified, launch 16 threads for optimization
    [==================================================] 100%
    2023-01-10 11:03:50,301 INFO consumed time 1.09413
    2023-01-10 11:03:50,416 INFO FPS=9.6, latency = 104172.3 us   (see ./.hb_check/torch_jit_subgraph_0.html)
    2023-01-10 11:03:50,552 INFO [Tue Jan 10 11:03:50 2023] End to compile the model with march bernoulli2.
    2023-01-10 11:03:50,553 INFO The converted model node information:
    ==============================================================================================
    Node                                                ON   Subgraph  Type                       
    ----------------------------------------------------------------------------------------------
    Slice_5                                             CPU  --        Slice                      
    Slice_10                                            CPU  --        Slice                      
    Slice_15                                            CPU  --        Slice                      
    Slice_20                                            CPU  --        Slice                      
    Slice_25                                            CPU  --        Slice                      
    Slice_30                                            CPU  --        Slice                      
    Slice_35                                            CPU  --        Slice                      
    Slice_40                                            CPU  --        Slice                      
    Concat_41                                           CPU  --        Concat                     
    Conv_42                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_43                                        BPU  id(0)     HzLeakyRelu                
    Conv_44                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_45                                        BPU  id(0)     HzLeakyRelu                
    Conv_46                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_47                                        BPU  id(0)     HzLeakyRelu                
    Conv_48                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_49                                        BPU  id(0)     HzLeakyRelu                
    Conv_50                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_51                                        BPU  id(0)     HzLeakyRelu                
    UNIT_CONV_FOR_Add_52                                BPU  id(0)     HzSQuantizedConv           
    Conv_53                                             BPU  id(0)     HzSQuantizedConv           
    Conv_54                                             BPU  id(0)     HzSQuantizedConv           
    Concat_55                                           BPU  id(0)     Concat                     
    LeakyRelu_57                                        BPU  id(0)     HzLeakyRelu                
    Conv_58                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_59                                        BPU  id(0)     HzLeakyRelu                
    Conv_60                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_61                                        BPU  id(0)     HzLeakyRelu                
    Conv_62                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_63                                        BPU  id(0)     HzLeakyRelu                
    Conv_64                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_65                                        BPU  id(0)     HzLeakyRelu                
    Conv_66                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_67                                        BPU  id(0)     HzLeakyRelu                
    UNIT_CONV_FOR_Add_68                                BPU  id(0)     HzSQuantizedConv           
    Conv_69                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_70                                        BPU  id(0)     HzLeakyRelu                
    Conv_71                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_72                                        BPU  id(0)     HzLeakyRelu                
    UNIT_CONV_FOR_Add_73                                BPU  id(0)     HzSQuantizedConv           
    Conv_74                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_75                                        BPU  id(0)     HzLeakyRelu                
    Conv_76                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_77                                        BPU  id(0)     HzLeakyRelu                
    UNIT_CONV_FOR_Add_78                                BPU  id(0)     HzSQuantizedConv           
    Conv_79                                             BPU  id(0)     HzSQuantizedConv           
    Conv_80                                             BPU  id(0)     HzSQuantizedConv           
    Concat_81                                           BPU  id(0)     Concat                     
    LeakyRelu_83                                        BPU  id(0)     HzLeakyRelu                
    Conv_84                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_85                                        BPU  id(0)     HzLeakyRelu                
    Conv_86                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_87                                        BPU  id(0)     HzLeakyRelu                
    Conv_88                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_89                                        BPU  id(0)     HzLeakyRelu                
    Conv_90                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_91                                        BPU  id(0)     HzLeakyRelu                
    Conv_92                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_93                                        BPU  id(0)     HzLeakyRelu                
    UNIT_CONV_FOR_Add_94                                BPU  id(0)     HzSQuantizedConv           
    Conv_95                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_96                                        BPU  id(0)     HzLeakyRelu                
    Conv_97                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_98                                        BPU  id(0)     HzLeakyRelu                
    UNIT_CONV_FOR_Add_99                                BPU  id(0)     HzSQuantizedConv           
    Conv_100                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_101                                       BPU  id(0)     HzLeakyRelu                
    Conv_102                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_103                                       BPU  id(0)     HzLeakyRelu                
    UNIT_CONV_FOR_Add_104                               BPU  id(0)     HzSQuantizedConv           
    Conv_105                                            BPU  id(0)     HzSQuantizedConv           
    Conv_106                                            BPU  id(0)     HzSQuantizedConv           
    Concat_107                                          BPU  id(0)     Concat                     
    LeakyRelu_109                                       BPU  id(0)     HzLeakyRelu                
    Conv_110                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_111                                       BPU  id(0)     HzLeakyRelu                
    Conv_112                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_113                                       BPU  id(0)     HzLeakyRelu                
    Conv_114                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_115                                       BPU  id(0)     HzLeakyRelu                
    MaxPool_116                                         BPU  id(0)     HzQuantizedMaxPool         
    MaxPool_117                                         BPU  id(0)     HzQuantizedMaxPool         
    MaxPool_118                                         BPU  id(0)     HzQuantizedMaxPool         
    Concat_119                                          BPU  id(0)     Concat                     
    Conv_120                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_121                                       BPU  id(0)     HzLeakyRelu                
    Conv_122                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_123                                       BPU  id(0)     HzLeakyRelu                
    Conv_124                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_125                                       BPU  id(0)     HzLeakyRelu                
    Conv_126                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_127                                       BPU  id(0)     HzLeakyRelu                
    Conv_128                                            BPU  id(0)     HzSQuantizedConv           
    Conv_129                                            BPU  id(0)     HzSQuantizedConv           
    Concat_130                                          BPU  id(0)     Concat                     
    LeakyRelu_132                                       BPU  id(0)     HzLeakyRelu                
    Conv_133                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_134                                       BPU  id(0)     HzLeakyRelu                
    Conv_135                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_136                                       BPU  id(0)     HzLeakyRelu                
    Resize_138                                          BPU  id(0)     HzQuantizedResizeUpsample  
    UNIT_CONV_FOR_onnx::Conv_279_0.03335_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv           
    Concat_139                                          BPU  id(0)     Concat                     
    Conv_140                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_141                                       BPU  id(0)     HzLeakyRelu                
    Conv_142                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_143                                       BPU  id(0)     HzLeakyRelu                
    Conv_144                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_145                                       BPU  id(0)     HzLeakyRelu                
    Conv_146                                            BPU  id(0)     HzSQuantizedConv           
    Conv_147                                            BPU  id(0)     HzSQuantizedConv           
    Concat_148                                          BPU  id(0)     Concat                     
    LeakyRelu_150                                       BPU  id(0)     HzLeakyRelu                
    Conv_151                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_152                                       BPU  id(0)     HzLeakyRelu                
    Conv_153                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_154                                       BPU  id(0)     HzLeakyRelu                
    Resize_156                                          BPU  id(0)     HzQuantizedResizeUpsample  
    Concat_157                                          BPU  id(0)     Concat                     
    Conv_158                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_159                                       BPU  id(0)     HzLeakyRelu                
    Conv_160                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_161                                       BPU  id(0)     HzLeakyRelu                
    Conv_162                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_163                                       BPU  id(0)     HzLeakyRelu                
    Conv_164                                            BPU  id(0)     HzSQuantizedConv           
    Conv_165                                            BPU  id(0)     HzSQuantizedConv           
    Concat_166                                          BPU  id(0)     Concat                     
    LeakyRelu_168                                       BPU  id(0)     HzLeakyRelu                
    Conv_169                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_170                                       BPU  id(0)     HzLeakyRelu                
    Conv_171                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_172                                       BPU  id(0)     HzLeakyRelu                
    ...CONV_FOR_onnx::Resize_325_0.03978_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv           
    Concat_173                                          BPU  id(0)     Concat                     
    Conv_174                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_175                                       BPU  id(0)     HzLeakyRelu                
    Conv_176                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_177                                       BPU  id(0)     HzLeakyRelu                
    Conv_178                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_179                                       BPU  id(0)     HzLeakyRelu                
    Conv_180                                            BPU  id(0)     HzSQuantizedConv           
    Conv_181                                            BPU  id(0)     HzSQuantizedConv           
    Concat_182                                          BPU  id(0)     Concat                     
    LeakyRelu_184                                       BPU  id(0)     HzLeakyRelu                
    Conv_185                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_186                                       BPU  id(0)     HzLeakyRelu                
    Conv_187                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_188                                       BPU  id(0)     HzLeakyRelu                
    Concat_189                                          BPU  id(0)     Concat                     
    Conv_190                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_191                                       BPU  id(0)     HzLeakyRelu                
    Conv_192                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_193                                       BPU  id(0)     HzLeakyRelu                
    Conv_194                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_195                                       BPU  id(0)     HzLeakyRelu                
    Conv_196                                            BPU  id(0)     HzSQuantizedConv           
    Conv_197                                            BPU  id(0)     HzSQuantizedConv           
    Concat_198                                          BPU  id(0)     Concat                     
    LeakyRelu_200                                       BPU  id(0)     HzLeakyRelu                
    Conv_201                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_202                                       BPU  id(0)     HzLeakyRelu                
    Conv_203                                            BPU  id(0)     HzSQuantizedConv           
    Reshape_204                                         CPU  --        Reshape                    
    Transpose_205                                       CPU  --        Transpose                  
    Conv_206                                            BPU  id(0)     HzSQuantizedConv           
    Reshape_207                                         CPU  --        Reshape                    
    Transpose_208                                       CPU  --        Transpose                  
    Conv_209                                            BPU  id(0)     HzSQuantizedConv           
    Reshape_210                                         CPU  --        Reshape                    
    Transpose_211                                       CPU  --        Transpose
    2023-01-10 11:03:50,555 INFO [Tue Jan 10 11:03:50 2023] End to Horizon NN Model Convert.
    2023-01-10 11:03:50,559 INFO ONNX model output num : 3
    2023-01-10 11:03:50,567 INFO End model checking....
    ```
    

- 改后输出
    
    ```bash
    cd $(dirname $0) || exit
    
    MODEL_NAME=${1:-yolov5s}
    
    model_type="onnx"
    onnx_model="./models/$MODEL_NAME.onnx"
    march="bernoulli2"
    
    hb_mapper checker --model-type ${model_type} \
                      --model ${onnx_model} \
                      --march ${march}
    /usr/local/lib/python3.6/site-packages/paramiko/transport.py:33: CryptographyDeprecationWarning: Python 3.6 is no longer supported by the Python core team. Therefore, support for it is deprecated in cryptography and will be removed in a future release.
      from cryptography.hazmat.backends import default_backend
    2023-01-10 12:19:43,654 INFO log will be stored in /open_explorer/smart_vision/hb_mapper_checker.log
    2023-01-10 12:19:43,654 INFO Start hb_mapper....
    2023-01-10 12:19:43,654 INFO hbdk version 3.41.4
    2023-01-10 12:19:43,654 INFO horizon_nn version 0.15.3
    2023-01-10 12:19:43,654 INFO hb_mapper version 1.13.3
    2023-01-10 12:19:43,674 INFO Model type: onnx
    2023-01-10 12:19:43,674 INFO input names []
    2023-01-10 12:19:43,674 INFO input shapes {}
    2023-01-10 12:19:43,674 INFO Begin model checking....
    2023-01-10 12:19:43,684 INFO [Tue Jan 10 12:19:43 2023] Start to Horizon NN Model Convert.
    2023-01-10 12:19:43,684 INFO The input parameter is not specified, convert with default parameters.
    2023-01-10 12:19:43,684 INFO Parsing the hbdk parameter:{'hbdk_pass_through_params': '--O0'}
    2023-01-10 12:19:43,684 INFO HorizonNN version: 0.15.3
    2023-01-10 12:19:43,684 INFO HBDK version: 3.41.4
    2023-01-10 12:19:43,685 INFO [Tue Jan 10 12:19:43 2023] Start to parse the onnx model.
    2023-01-10 12:19:43,702 INFO Input ONNX model infomation:
    ONNX IR version:          6
    Opset version:            [11]
    Producer:                 pytorch1.12.1
    Domain:                   none
    Input name:               data, [1, 3, 672, 672]
    Output name:              output, [1, 84, 84, 255]
    Output name:              380, [1, 42, 42, 255]
    Output name:              382, [1, 21, 21, 255]
    2023-01-10 12:19:43,804 INFO [Tue Jan 10 12:19:43 2023] End to parse the onnx model.
    2023-01-10 12:19:43,804 INFO Model input names parsed from model: ['data']
    2023-01-10 12:19:43,818 INFO Saving the original float model: ./.hb_check/original_float_model.onnx.
    2023-01-10 12:19:43,818 INFO [Tue Jan 10 12:19:43 2023] Start to optimize the model.
    2023-01-10 12:19:44,201 INFO [Tue Jan 10 12:19:44 2023] End to optimize the model.
    2023-01-10 12:19:44,216 INFO Saving the optimized model: ./.hb_check/optimized_float_model.onnx.
    2023-01-10 12:19:44,217 INFO [Tue Jan 10 12:19:44 2023] Start to calibrate the model.
    2023-01-10 12:19:44,222 INFO There are 1 samples in the calibration data set.
    2023-01-10 12:19:44,366 INFO Run calibration model with max method.
    max calibration in progress: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  4.21it/s]
    2023-01-10 12:19:44,806 INFO [Tue Jan 10 12:19:44 2023] End to calibrate the model.
    2023-01-10 12:19:44,807 INFO [Tue Jan 10 12:19:44 2023] Start to quantize the model.
    2023-01-10 12:19:45,900 INFO [Tue Jan 10 12:19:45 2023] End to quantize the model.
    2023-01-10 12:19:46,075 INFO Saving the quantized model: ./.hb_check/quantized_model.onnx.
    2023-01-10 12:19:46,597 INFO [Tue Jan 10 12:19:46 2023] Start to compile the model with march bernoulli2.
    2023-01-10 12:19:46,842 INFO Compile submodel: torch_jit_subgraph_0
    2023-01-10 12:19:47,212 INFO hbdk-cc parameters:['--O0', '--input-layout', 'NHWC', '--output-layout', 'NHWC']
    2023-01-10 12:19:47,239 INFO INFO: "-j" or "--jobs" is not specified, launch 16 threads for optimization
    [==================================================] 100%
    2023-01-10 12:19:48,270 INFO consumed time 1.0345
    2023-01-10 12:19:48,379 INFO FPS=10.37, latency = 96402.8 us   (see ./.hb_check/torch_jit_subgraph_0.html)
    2023-01-10 12:19:48,519 INFO [Tue Jan 10 12:19:48 2023] End to compile the model with march bernoulli2.
    2023-01-10 12:19:48,520 INFO The converted model node information:
    ==============================================================================================
    Node                                                ON   Subgraph  Type                       
    ----------------------------------------------------------------------------------------------
    Slice_5                                             CPU  --        Slice                      
    Slice_10                                            CPU  --        Slice                      
    Slice_15                                            CPU  --        Slice                      
    Slice_20                                            CPU  --        Slice                      
    Slice_25                                            CPU  --        Slice                      
    Slice_30                                            CPU  --        Slice                      
    Slice_35                                            CPU  --        Slice                      
    Slice_40                                            CPU  --        Slice                      
    Concat_41                                           CPU  --        Concat                     
    Conv_42                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_43                                        BPU  id(0)     HzLeakyRelu                
    Conv_44                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_45                                        BPU  id(0)     HzLeakyRelu                
    Conv_46                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_47                                        BPU  id(0)     HzLeakyRelu                
    Conv_48                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_49                                        BPU  id(0)     HzLeakyRelu                
    Conv_50                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_51                                        BPU  id(0)     HzLeakyRelu                
    UNIT_CONV_FOR_Add_52                                BPU  id(0)     HzSQuantizedConv           
    Conv_53                                             BPU  id(0)     HzSQuantizedConv           
    Conv_54                                             BPU  id(0)     HzSQuantizedConv           
    Concat_55                                           BPU  id(0)     Concat                     
    LeakyRelu_57                                        BPU  id(0)     HzLeakyRelu                
    Conv_58                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_59                                        BPU  id(0)     HzLeakyRelu                
    Conv_60                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_61                                        BPU  id(0)     HzLeakyRelu                
    Conv_62                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_63                                        BPU  id(0)     HzLeakyRelu                
    Conv_64                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_65                                        BPU  id(0)     HzLeakyRelu                
    Conv_66                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_67                                        BPU  id(0)     HzLeakyRelu                
    UNIT_CONV_FOR_Add_68                                BPU  id(0)     HzSQuantizedConv           
    Conv_69                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_70                                        BPU  id(0)     HzLeakyRelu                
    Conv_71                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_72                                        BPU  id(0)     HzLeakyRelu                
    UNIT_CONV_FOR_Add_73                                BPU  id(0)     HzSQuantizedConv           
    Conv_74                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_75                                        BPU  id(0)     HzLeakyRelu                
    Conv_76                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_77                                        BPU  id(0)     HzLeakyRelu                
    UNIT_CONV_FOR_Add_78                                BPU  id(0)     HzSQuantizedConv           
    Conv_79                                             BPU  id(0)     HzSQuantizedConv           
    Conv_80                                             BPU  id(0)     HzSQuantizedConv           
    Concat_81                                           BPU  id(0)     Concat                     
    LeakyRelu_83                                        BPU  id(0)     HzLeakyRelu                
    Conv_84                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_85                                        BPU  id(0)     HzLeakyRelu                
    Conv_86                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_87                                        BPU  id(0)     HzLeakyRelu                
    Conv_88                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_89                                        BPU  id(0)     HzLeakyRelu                
    Conv_90                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_91                                        BPU  id(0)     HzLeakyRelu                
    Conv_92                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_93                                        BPU  id(0)     HzLeakyRelu                
    UNIT_CONV_FOR_Add_94                                BPU  id(0)     HzSQuantizedConv           
    Conv_95                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_96                                        BPU  id(0)     HzLeakyRelu                
    Conv_97                                             BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_98                                        BPU  id(0)     HzLeakyRelu                
    UNIT_CONV_FOR_Add_99                                BPU  id(0)     HzSQuantizedConv           
    Conv_100                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_101                                       BPU  id(0)     HzLeakyRelu                
    Conv_102                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_103                                       BPU  id(0)     HzLeakyRelu                
    UNIT_CONV_FOR_Add_104                               BPU  id(0)     HzSQuantizedConv           
    Conv_105                                            BPU  id(0)     HzSQuantizedConv           
    Conv_106                                            BPU  id(0)     HzSQuantizedConv           
    Concat_107                                          BPU  id(0)     Concat                     
    LeakyRelu_109                                       BPU  id(0)     HzLeakyRelu                
    Conv_110                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_111                                       BPU  id(0)     HzLeakyRelu                
    Conv_112                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_113                                       BPU  id(0)     HzLeakyRelu                
    Conv_114                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_115                                       BPU  id(0)     HzLeakyRelu                
    MaxPool_116                                         BPU  id(0)     HzQuantizedMaxPool         
    MaxPool_117                                         BPU  id(0)     HzQuantizedMaxPool         
    MaxPool_118                                         BPU  id(0)     HzQuantizedMaxPool         
    Concat_119                                          BPU  id(0)     Concat                     
    Conv_120                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_121                                       BPU  id(0)     HzLeakyRelu                
    Conv_122                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_123                                       BPU  id(0)     HzLeakyRelu                
    Conv_124                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_125                                       BPU  id(0)     HzLeakyRelu                
    Conv_126                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_127                                       BPU  id(0)     HzLeakyRelu                
    Conv_128                                            BPU  id(0)     HzSQuantizedConv           
    Conv_129                                            BPU  id(0)     HzSQuantizedConv           
    Concat_130                                          BPU  id(0)     Concat                     
    LeakyRelu_132                                       BPU  id(0)     HzLeakyRelu                
    Conv_133                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_134                                       BPU  id(0)     HzLeakyRelu                
    Conv_135                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_136                                       BPU  id(0)     HzLeakyRelu                
    Resize_138                                          BPU  id(0)     HzQuantizedResizeUpsample  
    Concat_139                                          BPU  id(0)     Concat                     
    Conv_140                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_141                                       BPU  id(0)     HzLeakyRelu                
    Conv_142                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_143                                       BPU  id(0)     HzLeakyRelu                
    Conv_144                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_145                                       BPU  id(0)     HzLeakyRelu                
    Conv_146                                            BPU  id(0)     HzSQuantizedConv           
    Conv_147                                            BPU  id(0)     HzSQuantizedConv           
    Concat_148                                          BPU  id(0)     Concat                     
    LeakyRelu_150                                       BPU  id(0)     HzLeakyRelu                
    Conv_151                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_152                                       BPU  id(0)     HzLeakyRelu                
    Conv_153                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_154                                       BPU  id(0)     HzLeakyRelu                
    Resize_156                                          BPU  id(0)     HzQuantizedResizeUpsample  
    Concat_157                                          BPU  id(0)     Concat                     
    Conv_158                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_159                                       BPU  id(0)     HzLeakyRelu                
    Conv_160                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_161                                       BPU  id(0)     HzLeakyRelu                
    Conv_162                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_163                                       BPU  id(0)     HzLeakyRelu                
    Conv_164                                            BPU  id(0)     HzSQuantizedConv           
    Conv_165                                            BPU  id(0)     HzSQuantizedConv           
    Concat_166                                          BPU  id(0)     Concat                     
    LeakyRelu_168                                       BPU  id(0)     HzLeakyRelu                
    Conv_169                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_170                                       BPU  id(0)     HzLeakyRelu                
    Conv_171                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_172                                       BPU  id(0)     HzLeakyRelu                
    ...CONV_FOR_onnx::Resize_325_0.04157_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv           
    Concat_173                                          BPU  id(0)     Concat                     
    Conv_174                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_175                                       BPU  id(0)     HzLeakyRelu                
    Conv_176                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_177                                       BPU  id(0)     HzLeakyRelu                
    Conv_178                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_179                                       BPU  id(0)     HzLeakyRelu                
    Conv_180                                            BPU  id(0)     HzSQuantizedConv           
    Conv_181                                            BPU  id(0)     HzSQuantizedConv           
    Concat_182                                          BPU  id(0)     Concat                     
    LeakyRelu_184                                       BPU  id(0)     HzLeakyRelu                
    Conv_185                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_186                                       BPU  id(0)     HzLeakyRelu                
    Conv_187                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_188                                       BPU  id(0)     HzLeakyRelu                
    ...CONV_FOR_onnx::Resize_304_0.03234_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv           
    Concat_189                                          BPU  id(0)     Concat                     
    Conv_190                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_191                                       BPU  id(0)     HzLeakyRelu                
    Conv_192                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_193                                       BPU  id(0)     HzLeakyRelu                
    Conv_194                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_195                                       BPU  id(0)     HzLeakyRelu                
    Conv_196                                            BPU  id(0)     HzSQuantizedConv           
    Conv_197                                            BPU  id(0)     HzSQuantizedConv           
    Concat_198                                          BPU  id(0)     Concat                     
    LeakyRelu_200                                       BPU  id(0)     HzLeakyRelu                
    Conv_201                                            BPU  id(0)     HzSQuantizedConv           
    LeakyRelu_202                                       BPU  id(0)     HzLeakyRelu                
    Conv_203                                            BPU  id(0)     HzSQuantizedConv           
    Conv_205                                            BPU  id(0)     HzSQuantizedConv           
    Conv_207                                            BPU  id(0)     HzSQuantizedConv
    2023-01-10 12:19:48,521 INFO [Tue Jan 10 12:19:48 2023] End to Horizon NN Model Convert.
    2023-01-10 12:19:48,526 INFO ONNX model output num : 3
    2023-01-10 12:19:48,535 INFO End model checking....
    ```
    

可见改动对模型检查结果产生了影响，改动前网络最后部分层使用CPU，改后全部使用BPU（可能部分层不再在网络中体现，而是依赖之后额外实现后处理）

<aside>
💡 后续研究已经证明，使用 `export.py` 时会使用 `yolo.py` 中的网络结构定义。在v7.0版本的yolov5中， `Detect` 类的 `forward` 函数定义如下。注意其中已参照地平线的处理方式对 `x[i]` 做出修改，这样就能保证生成的模型兼容地平线在OE发布包中提供的转换及推理代码。其他相关修改参见以下比较（main分支为针对X3派定制的分支，master分支为YOLOv5官方主分支）：

[](https://github.com/SOTA-Robotics/yolov5/compare/master...main)

```python
def forward(self, x):
    z = []  # inference output
    for i in range(self.nl):
        x[i] = self.m[i](x[i])  # conv
        bs, _, ny, nx = x[i].shape  # x(bs,255,20,20) to x(bs,3,20,20,85)
        # x[i] = x[i].view(bs, self.na, self.no, ny, nx).permute(0, 1, 3, 4, 2).contiguous()
        x[i] = x[i].permute(0, 2, 3, 1).contiguous()

    #     if not self.training:  # inference
    #         if self.dynamic or self.grid[i].shape[2:4] != x[i].shape[2:4]:
    #             self.grid[i], self.anchor_grid[i] = self._make_grid(nx, ny, i)
    #
    #         if isinstance(self, Segment):  # (boxes + masks)
    #             xy, wh, conf, mask = x[i].split((2, 2, self.nc + 1, self.no - self.nc - 5), 4)
    #             xy = (xy.sigmoid() * 2 + self.grid[i]) * self.stride[i]  # xy
    #             wh = (wh.sigmoid() * 2) ** 2 * self.anchor_grid[i]  # wh
    #             y = torch.cat((xy, wh, conf.sigmoid(), mask), 4)
    #         else:  # Detect (boxes only)
    #             xy, wh, conf = x[i].sigmoid().split((2, 2, self.nc + 1), 4)
    #             xy = (xy * 2 + self.grid[i]) * self.stride[i]  # xy
    #             wh = (wh * 2) ** 2 * self.anchor_grid[i]  # wh
    #             y = torch.cat((xy, wh, conf), 4)
    #         z.append(y.view(bs, self.na * nx * ny, self.no))
    #
    # return x if self.training else (torch.cat(z, 1),) if self.export else (torch.cat(z, 1), x)
    return x
```

</aside>

未做修改时 `bash 03_build.sh` 的输出，其中出现以下警告信息：

<aside>
⚠️ 2023-01-10 11:25:59.341249719 [E:onnxruntime:, sequential_executor.cc:183 Execute] Non-zero status code returned while running Reshape node. Name:'Reshape_210' Status Message: /home/jenkins/agent/workspace/model_convert/onnxruntime/onnxruntime/core/providers/cpu/tensor/reshape_helper.h:43 onnxruntime::ReshapeHelper::ReshapeHelper(const onnxruntime::TensorShape&, std::vector<long int>&) gsl::narrow_cast<int64_t>(input_shape.Size()) == size was false. The input tensor cannot be reshaped to the requested shape. Input shape:{8,255,21,21}, requested shape:{1,3,85,21,21}

</aside>

做出修改后，不再出现该信息。

- `bash 04_inference.sh` 得到的图像
    
    ![demo.jpg](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/a3102d3d-048e-4a49-b36a-c955e0dd4869/demo.jpg)
    

- 改后inference结果图像（**识别正常！**）
    
    ![demo.jpg](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/59d360d6-762e-46e8-acb0-2e534b36794e/demo.jpg)
    

## PT转ONNX（v7.0）

本部分主要检验以上基于v2.0版的实验对于最新版的转换是否也有参考价值。在转换前对YOLOv5代码做出以下修改：

[](https://github.com/SOTA-Robotics/yolov5/compare/master...main)

之后，正常运行以下脚本进行模型转换：

```bash
python ./export.py --weights ./weights/yolov5s-latest.pt --include onnx --opset 11
```

```bash
export: data=data/coco128.yaml, weights=['./weights/yolov5s-latest.pt'], imgsz=[672, 672], batch_size=1, device=cpu, half=False, inplace=False, keras=False, optimize=False, int8=False, dynamic=False, simplify=False, opset=11, verbose=False, workspace=4, nms=False, agnostic_nms=False, topk_per_class=100, topk_all=100, iou_thres=0.45, conf_thres=0.25, include=['onnx']
YOLOv5 🚀 v7.0-66-g11d63e3 Python-3.8.10 torch-1.12.1+cu116 CPU

Fusing layers... 
YOLOv5s summary: 213 layers, 7225885 parameters, 0 gradients, 16.4 GFLOPs

PyTorch: starting from weights/yolov5s-latest.pt with output shape (1, 84, 84, 255) (14.1 MB)

ONNX: starting export with onnx 1.12.0...
ONNX: export success ✅ 0.8s, saved as weights/yolov5s-latest.onnx (27.6 MB)

Export complete (2.9s)
Results saved to /home/dzp/yolov5/weights
Detect:          python detect.py --weights weights/yolov5s-latest.onnx 
Validate:        python val.py --weights weights/yolov5s-latest.onnx 
PyTorch Hub:     model = torch.hub.load('ultralytics/yolov5', 'custom', 'weights/yolov5s-latest.onnx')  
Visualize:       https://netron.app
```

```bash
export: data=data/coco128.yaml, weights=['./models/yolov5s.pt'], imgsz=[640, 640], batch_size=1, device=cpu, half=False, inplace=False, keras=False, optimize=False, int8=False, dynamic=False, simplify=False, opset=11, verbose=False, workspace=4, nms=False, agnostic_nms=False, topk_per_class=100, topk_all=100, iou_thres=0.45, conf_thres=0.25, include=['onnx']
YOLOv5 🚀 v7.0-56-gc0ca1d2 Python-3.8.10 torch-1.12.1+cu116 CPU

Fusing layers... 
YOLOv5s summary: 213 layers, 7225885 parameters, 0 gradients

PyTorch: starting from models/yolov5s.pt with output shape (1, 25200, 85) (14.1 MB)

ONNX: starting export with onnx 1.12.0...
ONNX: export success ✅ 0.9s, saved as models/yolov5s.onnx (28.0 MB)

Export complete (1.2s)
Results saved to /home/dzp/yolov5/models
Detect:          python detect.py --weights models/yolov5s.onnx 
Validate:        python val.py --weights models/yolov5s.onnx 
PyTorch Hub:     model = torch.hub.load('ultralytics/yolov5', 'custom', 'models/yolov5s.onnx')  
Visualize:       https://netron.app
```

## 将v7.0 ONNX转换为bin

1. 进入OE容器（[准备开发环境](https://www.notion.so/27e5449af9af4b07853f44b8dbe7eb00) ）；
2. 对转换得到的ONNX，使用 `01_check.sh` 进行检验
    - 检验输出
        
        ```bash
        cd $(dirname $0) || exit
        
        MODEL_NAME=${1:-yolov5s}
        
        model_type="onnx"
        onnx_model="./models/$MODEL_NAME-latest.onnx"
        march="bernoulli2"
        
        hb_mapper checker --model-type ${model_type} \
                          --model ${onnx_model} \
                          --march ${march}
        /usr/local/lib/python3.6/site-packages/paramiko/transport.py:33: CryptographyDeprecationWarning: Python 3.6 is no longer supported by the Python core team. Therefore, support for it is deprecated in cryptography and will be removed in a future release.
          from cryptography.hazmat.backends import default_backend
        2023-01-10 19:05:01,477 INFO log will be stored in /open_explorer/smart_vision/hb_mapper_checker.log
        2023-01-10 19:05:01,477 INFO Start hb_mapper....
        2023-01-10 19:05:01,477 INFO hbdk version 3.41.4
        2023-01-10 19:05:01,477 INFO horizon_nn version 0.15.3
        2023-01-10 19:05:01,477 INFO hb_mapper version 1.13.3
        2023-01-10 19:05:01,496 INFO Model type: onnx
        2023-01-10 19:05:01,496 INFO input names []
        2023-01-10 19:05:01,496 INFO input shapes {}
        2023-01-10 19:05:01,496 INFO Begin model checking....
        2023-01-10 19:05:01,506 INFO [Tue Jan 10 19:05:01 2023] Start to Horizon NN Model Convert.
        2023-01-10 19:05:01,507 INFO The input parameter is not specified, convert with default parameters.
        2023-01-10 19:05:01,507 INFO Parsing the hbdk parameter:{'hbdk_pass_through_params': '--O0'}
        2023-01-10 19:05:01,507 INFO HorizonNN version: 0.15.3
        2023-01-10 19:05:01,507 INFO HBDK version: 3.41.4
        2023-01-10 19:05:01,507 INFO [Tue Jan 10 19:05:01 2023] Start to parse the onnx model.
        2023-01-10 19:05:01,523 INFO Input ONNX model infomation:
        ONNX IR version:          6
        Opset version:            [11]
        Producer:                 pytorch1.12.1
        Domain:                   none
        Input name:               data, [1, 3, 672, 672]
        Output name:              output0, [1, 84, 84, 255]
        Output name:              332, [1, 42, 42, 255]
        Output name:              334, [1, 21, 21, 255]
        2023-01-10 19:05:01,616 INFO [Tue Jan 10 19:05:01 2023] End to parse the onnx model.
        2023-01-10 19:05:01,616 INFO Model input names parsed from model: ['data']
        2023-01-10 19:05:01,639 INFO Saving the original float model: ./.hb_check/original_float_model.onnx.
        2023-01-10 19:05:01,639 INFO [Tue Jan 10 19:05:01 2023] Start to optimize the model.
        2023-01-10 19:05:01,903 INFO [Tue Jan 10 19:05:01 2023] End to optimize the model.
        2023-01-10 19:05:01,925 INFO Saving the optimized model: ./.hb_check/optimized_float_model.onnx.
        2023-01-10 19:05:01,925 INFO [Tue Jan 10 19:05:01 2023] Start to calibrate the model.
        2023-01-10 19:05:01,931 INFO There are 1 samples in the calibration data set.
        2023-01-10 19:05:02,046 INFO Run calibration model with max method.
        max calibration in progress: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  4.97it/s]
        2023-01-10 19:05:02,533 INFO [Tue Jan 10 19:05:02 2023] End to calibrate the model.
        2023-01-10 19:05:02,534 INFO [Tue Jan 10 19:05:02 2023] Start to quantize the model.
        2023-01-10 19:05:03,590 INFO [Tue Jan 10 19:05:03 2023] End to quantize the model.
        2023-01-10 19:05:03,777 INFO Saving the quantized model: ./.hb_check/quantized_model.onnx.
        2023-01-10 19:05:04,307 INFO [Tue Jan 10 19:05:04 2023] Start to compile the model with march bernoulli2.
        2023-01-10 19:05:04,541 INFO Compile submodel: torch_jit_subgraph_0
        2023-01-10 19:05:04,895 INFO hbdk-cc parameters:['--O0', '--input-layout', 'NHWC', '--output-layout', 'NHWC']
        2023-01-10 19:05:04,925 INFO INFO: "-j" or "--jobs" is not specified, launch 16 threads for optimization
        2023-01-10 19:05:05,062 INFO INFO: Layer "Mul_3" will be executed on CPU
        2023-01-10 19:05:05,062 INFO INFO: Layer "Mul_6" will be executed on CPU
        2023-01-10 19:05:05,062 INFO INFO: Layer "Mul_9" will be executed on CPU
        2023-01-10 19:05:05,062 INFO INFO: Layer "Mul_19" will be executed on CPU
        2023-01-10 19:05:05,062 INFO INFO: Layer "Mul_12" will be executed on CPU
        2023-01-10 19:05:05,062 INFO INFO: Layer "Mul_15" will be executed on CPU
        2023-01-10 19:05:05,062 INFO INFO: Layer "Mul_23" will be executed on CPU
        2023-01-10 19:05:05,062 INFO INFO: Layer "Mul_26" will be executed on CPU
        2023-01-10 19:05:05,062 INFO INFO: Layer "Mul_29" will be executed on CPU
        2023-01-10 19:05:05,062 INFO INFO: Layer "Mul_46" will be executed on CPU
        2023-01-10 19:05:05,062 INFO INFO: Layer "Mul_32" will be executed on CPU
        2023-01-10 19:05:05,063 INFO INFO: Layer "Mul_35" will be executed on CPU
        2023-01-10 19:05:05,063 INFO INFO: Layer "Mul_39" will be executed on CPU
        2023-01-10 19:05:05,063 INFO INFO: Layer "Mul_42" will be executed on CPU
        2023-01-10 19:05:05,063 INFO INFO: Layer "Mul_50" will be executed on CPU
        2023-01-10 19:05:05,063 INFO INFO: Layer "Mul_53" will be executed on CPU
        2023-01-10 19:05:05,063 INFO INFO: Layer "Mul_56" will be executed on CPU
        2023-01-10 19:05:05,063 INFO INFO: Layer "Mul_80" will be executed on CPU
        2023-01-10 19:05:05,063 INFO INFO: Layer "Mul_59" will be executed on CPU
        2023-01-10 19:05:05,063 INFO INFO: Layer "Mul_62" will be executed on CPU
        2023-01-10 19:05:05,063 INFO INFO: Layer "Mul_66" will be executed on CPU
        2023-01-10 19:05:05,063 INFO INFO: Layer "Mul_69" will be executed on CPU
        2023-01-10 19:05:05,063 INFO INFO: Layer "Mul_73" will be executed on CPU
        2023-01-10 19:05:05,064 INFO INFO: Layer "Mul_76" will be executed on CPU
        2023-01-10 19:05:05,064 INFO INFO: Layer "Mul_84" will be executed on CPU
        2023-01-10 19:05:05,064 INFO INFO: Layer "Mul_87" will be executed on CPU
        2023-01-10 19:05:05,064 INFO INFO: Layer "Mul_90" will be executed on CPU
        2023-01-10 19:05:05,064 INFO INFO: Layer "Mul_100" will be executed on CPU
        2023-01-10 19:05:05,064 INFO INFO: Layer "Mul_93" will be executed on CPU
        2023-01-10 19:05:05,064 INFO INFO: Layer "Mul_96" will be executed on CPU
        2023-01-10 19:05:05,064 INFO INFO: Layer "Mul_104" will be executed on CPU
        2023-01-10 19:05:05,064 INFO INFO: Layer "Mul_107" will be executed on CPU
        2023-01-10 19:05:05,064 INFO INFO: Layer "Mul_114" will be executed on CPU
        2023-01-10 19:05:05,064 INFO INFO: Layer "Mul_117" will be executed on CPU
        2023-01-10 19:05:05,064 INFO INFO: Layer "Mul_123" will be executed on CPU
        2023-01-10 19:05:05,064 INFO INFO: Layer "Mul_132" will be executed on CPU
        2023-01-10 19:05:05,065 INFO INFO: Layer "Mul_126" will be executed on CPU
        2023-01-10 19:05:05,065 INFO INFO: Layer "Mul_129" will be executed on CPU
        2023-01-10 19:05:05,065 INFO INFO: Layer "Mul_136" will be executed on CPU
        2023-01-10 19:05:05,065 INFO INFO: Layer "Mul_139" will be executed on CPU
        2023-01-10 19:05:05,065 INFO INFO: Layer "Mul_145" will be executed on CPU
        2023-01-10 19:05:05,065 INFO INFO: Layer "Mul_154" will be executed on CPU
        2023-01-10 19:05:05,065 INFO INFO: Layer "Mul_148" will be executed on CPU
        2023-01-10 19:05:05,065 INFO INFO: Layer "Mul_151" will be executed on CPU
        2023-01-10 19:05:05,065 INFO INFO: Layer "Mul_158" will be executed on CPU
        2023-01-10 19:05:05,065 INFO INFO: Layer "Mul_161" will be executed on CPU
        2023-01-10 19:05:05,065 INFO INFO: Layer "Mul_165" will be executed on CPU
        2023-01-10 19:05:05,065 INFO INFO: Layer "Mul_174" will be executed on CPU
        2023-01-10 19:05:05,066 INFO INFO: Layer "Mul_168" will be executed on CPU
        2023-01-10 19:05:05,066 INFO INFO: Layer "Mul_171" will be executed on CPU
        2023-01-10 19:05:05,066 INFO INFO: Layer "Mul_178" will be executed on CPU
        2023-01-10 19:05:05,066 INFO INFO: Layer "Mul_181" will be executed on CPU
        2023-01-10 19:05:05,066 INFO INFO: Layer "Mul_185" will be executed on CPU
        2023-01-10 19:05:05,066 INFO INFO: Layer "Mul_194" will be executed on CPU
        2023-01-10 19:05:05,066 INFO INFO: Layer "Mul_188" will be executed on CPU
        2023-01-10 19:05:05,066 INFO INFO: Layer "Mul_191" will be executed on CPU
        2023-01-10 19:05:05,066 INFO INFO: Layer "Mul_198" will be executed on CPU
        [==================================================] 100%
        2023-01-10 19:05:05,486 INFO consumed time 0.565374
        2023-01-10 19:05:05,552 WARNING Performance information does not include operators in the model running on the CPU (including HzLut whose shape is over 8192)
        2023-01-10 19:05:05,587 INFO FPS=14.73, latency = 67885.9 us   (see ./.hb_check/torch_jit_subgraph_0.html)
        2023-01-10 19:05:05,713 INFO [Tue Jan 10 19:05:05 2023] End to compile the model with march bernoulli2.
        2023-01-10 19:05:05,714 INFO The converted model node information:
        ==============================================================================================
        Node                                                ON   Subgraph  Type                       
        ----------------------------------------------------------------------------------------------
        Conv_1                                              BPU  id(0)     HzSQuantizedConv           
        Mul_3                                               BPU  id(0)     HzLut                      
        Conv_4                                              BPU  id(0)     HzSQuantizedConv           
        Mul_6                                               BPU  id(0)     HzLut                      
        Conv_7                                              BPU  id(0)     HzSQuantizedConv           
        Mul_9                                               BPU  id(0)     HzLut                      
        Conv_10                                             BPU  id(0)     HzSQuantizedConv           
        Mul_12                                              BPU  id(0)     HzLut                      
        Conv_13                                             BPU  id(0)     HzSQuantizedConv           
        Mul_15                                              BPU  id(0)     HzLut                      
        UNIT_CONV_FOR_Add_16                                BPU  id(0)     HzSQuantizedConv           
        Conv_17                                             BPU  id(0)     HzSQuantizedConv           
        Mul_19                                              BPU  id(0)     HzLut                      
        ...CONV_FOR_onnx::Concat_143_0.20249_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv           
        Concat_20                                           BPU  id(0)     Concat                     
        Conv_21                                             BPU  id(0)     HzSQuantizedConv           
        Mul_23                                              BPU  id(0)     HzLut                      
        Conv_24                                             BPU  id(0)     HzSQuantizedConv           
        Mul_26                                              BPU  id(0)     HzLut                      
        Conv_27                                             BPU  id(0)     HzSQuantizedConv           
        Mul_29                                              BPU  id(0)     HzLut                      
        Conv_30                                             BPU  id(0)     HzSQuantizedConv           
        Mul_32                                              BPU  id(0)     HzLut                      
        Conv_33                                             BPU  id(0)     HzSQuantizedConv           
        Mul_35                                              BPU  id(0)     HzLut                      
        UNIT_CONV_FOR_Add_36                                BPU  id(0)     HzSQuantizedConv           
        Conv_37                                             BPU  id(0)     HzSQuantizedConv           
        Mul_39                                              BPU  id(0)     HzLut                      
        Conv_40                                             BPU  id(0)     HzSQuantizedConv           
        Mul_42                                              BPU  id(0)     HzLut                      
        UNIT_CONV_FOR_Add_43                                BPU  id(0)     HzSQuantizedConv           
        Conv_44                                             BPU  id(0)     HzSQuantizedConv           
        Mul_46                                              BPU  id(0)     HzLut                      
        ...CONV_FOR_onnx::Concat_170_0.04201_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv           
        Concat_47                                           BPU  id(0)     Concat                     
        Conv_48                                             BPU  id(0)     HzSQuantizedConv           
        Mul_50                                              BPU  id(0)     HzLut                      
        Conv_51                                             BPU  id(0)     HzSQuantizedConv           
        Mul_53                                              BPU  id(0)     HzLut                      
        Conv_54                                             BPU  id(0)     HzSQuantizedConv           
        Mul_56                                              BPU  id(0)     HzLut                      
        Conv_57                                             BPU  id(0)     HzSQuantizedConv           
        Mul_59                                              BPU  id(0)     HzLut                      
        Conv_60                                             BPU  id(0)     HzSQuantizedConv           
        Mul_62                                              BPU  id(0)     HzLut                      
        UNIT_CONV_FOR_Add_63                                BPU  id(0)     HzSQuantizedConv           
        Conv_64                                             BPU  id(0)     HzSQuantizedConv           
        Mul_66                                              BPU  id(0)     HzLut                      
        Conv_67                                             BPU  id(0)     HzSQuantizedConv           
        Mul_69                                              BPU  id(0)     HzLut                      
        UNIT_CONV_FOR_Add_70                                BPU  id(0)     HzSQuantizedConv           
        Conv_71                                             BPU  id(0)     HzSQuantizedConv           
        Mul_73                                              BPU  id(0)     HzLut                      
        Conv_74                                             BPU  id(0)     HzSQuantizedConv           
        Mul_76                                              BPU  id(0)     HzLut                      
        UNIT_CONV_FOR_Add_77                                BPU  id(0)     HzSQuantizedConv           
        Conv_78                                             BPU  id(0)     HzSQuantizedConv           
        Mul_80                                              BPU  id(0)     HzLut                      
        ...CONV_FOR_onnx::Concat_204_0.04423_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv           
        Concat_81                                           BPU  id(0)     Concat                     
        Conv_82                                             BPU  id(0)     HzSQuantizedConv           
        Mul_84                                              BPU  id(0)     HzLut                      
        Conv_85                                             BPU  id(0)     HzSQuantizedConv           
        Mul_87                                              BPU  id(0)     HzLut                      
        Conv_88                                             BPU  id(0)     HzSQuantizedConv           
        Mul_90                                              BPU  id(0)     HzLut                      
        Conv_91                                             BPU  id(0)     HzSQuantizedConv           
        Mul_93                                              BPU  id(0)     HzLut                      
        Conv_94                                             BPU  id(0)     HzSQuantizedConv           
        Mul_96                                              BPU  id(0)     HzLut                      
        UNIT_CONV_FOR_Add_97                                BPU  id(0)     HzSQuantizedConv           
        Conv_98                                             BPU  id(0)     HzSQuantizedConv           
        Mul_100                                             BPU  id(0)     HzLut                      
        ...CONV_FOR_onnx::Concat_224_0.03371_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv           
        Concat_101                                          BPU  id(0)     Concat                     
        Conv_102                                            BPU  id(0)     HzSQuantizedConv           
        Mul_104                                             BPU  id(0)     HzLut                      
        Conv_105                                            BPU  id(0)     HzSQuantizedConv           
        Mul_107                                             BPU  id(0)     HzLut                      
        MaxPool_108                                         BPU  id(0)     HzQuantizedMaxPool         
        MaxPool_109                                         BPU  id(0)     HzQuantizedMaxPool         
        MaxPool_110                                         BPU  id(0)     HzQuantizedMaxPool         
        Concat_111                                          BPU  id(0)     Concat                     
        Conv_112                                            BPU  id(0)     HzSQuantizedConv           
        Mul_114                                             BPU  id(0)     HzLut                      
        Conv_115                                            BPU  id(0)     HzSQuantizedConv           
        Mul_117                                             BPU  id(0)     HzLut                      
        Resize_119                                          BPU  id(0)     HzQuantizedResizeUpsample  
        ...CONV_FOR_onnx::Concat_246_0.03079_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv           
        UNIT_CONV_FOR_onnx::Conv_208_0.03079_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv           
        Concat_120                                          BPU  id(0)     Concat                     
        Conv_121                                            BPU  id(0)     HzSQuantizedConv           
        Mul_123                                             BPU  id(0)     HzLut                      
        Conv_124                                            BPU  id(0)     HzSQuantizedConv           
        Mul_126                                             BPU  id(0)     HzLut                      
        Conv_127                                            BPU  id(0)     HzSQuantizedConv           
        Mul_129                                             BPU  id(0)     HzLut                      
        Conv_130                                            BPU  id(0)     HzSQuantizedConv           
        Mul_132                                             BPU  id(0)     HzLut                      
        ...CONV_FOR_onnx::Concat_256_0.02170_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv           
        ...CONV_FOR_onnx::Concat_259_0.02170_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv           
        Concat_133                                          BPU  id(0)     Concat                     
        Conv_134                                            BPU  id(0)     HzSQuantizedConv           
        Mul_136                                             BPU  id(0)     HzLut                      
        Conv_137                                            BPU  id(0)     HzSQuantizedConv           
        Mul_139                                             BPU  id(0)     HzLut                      
        Resize_141                                          BPU  id(0)     HzQuantizedResizeUpsample  
        UNIT_CONV_FOR_onnx::Conv_174_0.02784_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv           
        Concat_142                                          BPU  id(0)     Concat                     
        Conv_143                                            BPU  id(0)     HzSQuantizedConv           
        Mul_145                                             BPU  id(0)     HzLut                      
        Conv_146                                            BPU  id(0)     HzSQuantizedConv           
        Mul_148                                             BPU  id(0)     HzLut                      
        Conv_149                                            BPU  id(0)     HzSQuantizedConv           
        Mul_151                                             BPU  id(0)     HzLut                      
        Conv_152                                            BPU  id(0)     HzSQuantizedConv           
        Mul_154                                             BPU  id(0)     HzLut                      
        ...CONV_FOR_onnx::Concat_281_0.03700_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv           
        ...CONV_FOR_onnx::Concat_284_0.03700_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv           
        Concat_155                                          BPU  id(0)     Concat                     
        Conv_156                                            BPU  id(0)     HzSQuantizedConv           
        Mul_158                                             BPU  id(0)     HzLut                      
        Conv_159                                            BPU  id(0)     HzSQuantizedConv           
        Mul_161                                             BPU  id(0)     HzLut                      
        ...CONV_FOR_onnx::Resize_266_0.03217_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv           
        Concat_162                                          BPU  id(0)     Concat                     
        Conv_163                                            BPU  id(0)     HzSQuantizedConv           
        Mul_165                                             BPU  id(0)     HzLut                      
        Conv_166                                            BPU  id(0)     HzSQuantizedConv           
        Mul_168                                             BPU  id(0)     HzLut                      
        Conv_169                                            BPU  id(0)     HzSQuantizedConv           
        Mul_171                                             BPU  id(0)     HzLut                      
        Conv_172                                            BPU  id(0)     HzSQuantizedConv           
        Mul_174                                             BPU  id(0)     HzLut                      
        ...CONV_FOR_onnx::Concat_301_0.02784_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv           
        ...CONV_FOR_onnx::Concat_304_0.02784_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv           
        Concat_175                                          BPU  id(0)     Concat                     
        Conv_176                                            BPU  id(0)     HzSQuantizedConv           
        Mul_178                                             BPU  id(0)     HzLut                      
        Conv_179                                            BPU  id(0)     HzSQuantizedConv           
        Mul_181                                             BPU  id(0)     HzLut                      
        ...CONV_FOR_onnx::Concat_311_0.03079_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv           
        ...CONV_FOR_onnx::Resize_241_0.03079_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv           
        Concat_182                                          BPU  id(0)     Concat                     
        Conv_183                                            BPU  id(0)     HzSQuantizedConv           
        Mul_185                                             BPU  id(0)     HzLut                      
        Conv_186                                            BPU  id(0)     HzSQuantizedConv           
        Mul_188                                             BPU  id(0)     HzLut                      
        Conv_189                                            BPU  id(0)     HzSQuantizedConv           
        Mul_191                                             BPU  id(0)     HzLut                      
        Conv_192                                            BPU  id(0)     HzSQuantizedConv           
        Mul_194                                             BPU  id(0)     HzLut                      
        ...CONV_FOR_onnx::Concat_321_0.05753_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv           
        ...CONV_FOR_onnx::Concat_324_0.05753_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv           
        Concat_195                                          BPU  id(0)     Concat                     
        Conv_196                                            BPU  id(0)     HzSQuantizedConv           
        Mul_198                                             BPU  id(0)     HzLut                      
        Conv_199                                            BPU  id(0)     HzSQuantizedConv           
        Conv_201                                            BPU  id(0)     HzSQuantizedConv           
        Conv_203                                            BPU  id(0)     HzSQuantizedConv
        2023-01-10 19:05:05,716 INFO [Tue Jan 10 19:05:05 2023] End to Horizon NN Model Convert.
        2023-01-10 19:05:05,720 INFO ONNX model output num : 3
        2023-01-10 19:05:05,730 INFO End model checking....
        ```
        
3. 在此基础上，依次进行后续的 `02_preprocess.sh` ， `03_build.sh` 脚本，build 脚本输出如下：
    - build 脚本输出，可见不再产生 `Non-zero status code returned while running Reshape node` 问题。
        
        ```bash
        cd $(dirname $0)
        
        MODEL_NAME=${1:-yolov5s}
        
        config_file="./configs/${MODEL_NAME}_config.yaml"
        model_type="onnx"
        
        # build model
        hb_mapper makertbin --config ${config_file}  \
                            --model-type ${model_type}
        /usr/local/lib/python3.6/site-packages/paramiko/transport.py:33: CryptographyDeprecationWarning: Python 3.6 is no longer supported by the Python core team. Therefore, support for it is deprecated in cryptography and will be removed in a future release.
          from cryptography.hazmat.backends import default_backend
        2023-01-10 19:23:43,399 INFO log will be stored in /open_explorer/smart_vision/hb_mapper_makertbin.log
        2023-01-10 19:23:43,399 INFO Start hb_mapper....
        2023-01-10 19:23:43,399 INFO hbdk version 3.41.4
        2023-01-10 19:23:43,399 INFO horizon_nn version 0.15.3
        2023-01-10 19:23:43,399 INFO hb_mapper version 1.13.3
        2023-01-10 19:23:43,399 INFO Start Model Convert....
        2023-01-10 19:23:43,406 INFO Using onnx model file: /open_explorer/smart_vision/models/yolov5s-latest.onnx
        2023-01-10 19:23:43,424 INFO Model has 1 inputs according to model file
        2023-01-10 19:23:43,424 INFO working_dir does not exist. Creating working_dir: /open_explorer/smart_vision/models/model_output
        2023-01-10 19:23:43,424 INFO Model name not given in yaml_file, using model name from model file: ['data']
        2023-01-10 19:23:43,424 INFO Model input shape not given in yaml_file, using shape from model file: [[1, 3, 672, 672]]
        2023-01-10 19:23:43,424 INFO nv12 input type rt received.
        2023-01-10 19:23:43,424 INFO custom_op does not exist, skipped
        2023-01-10 19:23:43,425 WARNING Input node data's input_source not set, it will be set to pyramid by default
        2023-01-10 19:23:43,426 WARNING Please note that the calibration file data type is set to float32, determined by the name of the calibration dir name suffix.
        2023-01-10 19:23:43,426 WARNING if you need to set it explicitly, please configure the value of cal_data_type in the calibration_parameters group in yaml.
        2023-01-10 19:23:43,426 INFO *******************************************
        2023-01-10 19:23:43,426 INFO First calibration picture name: COCO_val2014_000000181007.rgb
        2023-01-10 19:23:43,427 INFO First calibration picture md5:
        136bb23027c812cc2978395421fe6be7  /open_explorer/smart_vision/calibration_data_rgb_f32/COCO_val2014_000000181007.rgb
        2023-01-10 19:23:43,438 INFO *******************************************
        2023-01-10 19:23:45,370 INFO [Tue Jan 10 19:23:45 2023] Start to Horizon NN Model Convert.
        2023-01-10 19:23:45,370 INFO Parsing the input parameter:{'data': {'input_shape': [1, 3, 672, 672], 'expected_input_type': 'YUV444_128', 'original_input_type': 'RGB', 'original_input_layout': 'NCHW', 'scales': array([0.00392157], dtype=float32)}}
        2023-01-10 19:23:45,370 INFO Parsing the calibration parameter
        2023-01-10 19:23:45,370 INFO Parsing the hbdk parameter:{'hbdk_pass_through_params': '--O3 --core-num 1 --fast ', 'input-source': {'data': 'pyramid', '_default_value': 'ddr'}}
        2023-01-10 19:23:45,370 INFO HorizonNN version: 0.15.3
        2023-01-10 19:23:45,370 INFO HBDK version: 3.41.4
        2023-01-10 19:23:45,370 INFO [Tue Jan 10 19:23:45 2023] Start to parse the onnx model.
        2023-01-10 19:23:45,384 INFO Input ONNX model infomation:
        ONNX IR version:          6
        Opset version:            [11]
        Producer:                 pytorch1.12.1
        Domain:                   none
        Input name:               data, [1, 3, 672, 672]
        Output name:              output0, [1, 84, 84, 255]
        Output name:              332, [1, 42, 42, 255]
        Output name:              334, [1, 21, 21, 255]
        2023-01-10 19:23:45,479 INFO [Tue Jan 10 19:23:45 2023] End to parse the onnx model.
        2023-01-10 19:23:45,479 INFO Model input names parsed from model: ['data']
        2023-01-10 19:23:45,479 INFO Create a preprocessing operator for input_name data with means=None, std=[254.99998492], original_input_layout=NCHW, color convert from 'RGB' to 'YUV_BT601_FULL_RANGE'.
        2023-01-10 19:23:45,544 INFO Saving the original float model: yolov5s_672x672_nv12_original_float_model.onnx.
        2023-01-10 19:23:45,544 INFO [Tue Jan 10 19:23:45 2023] Start to optimize the model.
        2023-01-10 19:23:45,821 INFO [Tue Jan 10 19:23:45 2023] End to optimize the model.
        2023-01-10 19:23:45,834 INFO Saving the optimized model: yolov5s_672x672_nv12_optimized_float_model.onnx.
        2023-01-10 19:23:45,835 INFO [Tue Jan 10 19:23:45 2023] Start to calibrate the model.
        2023-01-10 19:23:45,835 INFO There are 50 samples in the calibration data set.
        2023-01-10 19:23:45,951 INFO Run calibration model with default calibration method.
        Default calibration in progress: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:28<00:00,  4.00s/it]
        2023-01-10 19:24:22,966 INFO Select kl method.
        2023-01-10 19:24:22,989 INFO [Tue Jan 10 19:24:22 2023] End to calibrate the model.
        2023-01-10 19:24:22,990 INFO [Tue Jan 10 19:24:22 2023] Start to quantize the model.
        2023-01-10 19:24:26,866 INFO input data is from pyramid. Its layout is set to NHWC
        2023-01-10 19:24:27,065 INFO [Tue Jan 10 19:24:27 2023] End to quantize the model.
        2023-01-10 19:24:27,232 INFO Saving the quantized model: yolov5s_672x672_nv12_quantized_model.onnx.
        2023-01-10 19:24:27,731 INFO [Tue Jan 10 19:24:27 2023] Start to compile the model with march bernoulli2.
        2023-01-10 19:24:27,956 INFO Compile submodel: torch_jit_subgraph_0
        2023-01-10 19:24:28,285 INFO hbdk-cc parameters:['--O3', '--core-num', '1', '--fast', '--input-layout', 'NHWC', '--output-layout', 'NHWC', '--input-source', 'pyramid']
        2023-01-10 19:24:28,317 INFO INFO: "-j" or "--jobs" is not specified, launch 16 threads for optimization
        2023-01-10 19:24:28,317 WARNING missing stride for pyramid input[0], use its aligned width by default.
        2023-01-10 19:24:28,453 INFO INFO: Layer "Mul_3" will be executed on CPU
        2023-01-10 19:24:28,453 INFO INFO: Layer "Mul_6" will be executed on CPU
        2023-01-10 19:24:28,453 INFO INFO: Layer "Mul_9" will be executed on CPU
        2023-01-10 19:24:28,453 INFO INFO: Layer "Mul_19" will be executed on CPU
        2023-01-10 19:24:28,453 INFO INFO: Layer "Mul_12" will be executed on CPU
        2023-01-10 19:24:28,453 INFO INFO: Layer "Mul_15" will be executed on CPU
        2023-01-10 19:24:28,453 INFO INFO: Layer "Mul_23" will be executed on CPU
        2023-01-10 19:24:28,453 INFO INFO: Layer "Mul_26" will be executed on CPU
        2023-01-10 19:24:28,454 INFO INFO: Layer "Mul_29" will be executed on CPU
        2023-01-10 19:24:28,454 INFO INFO: Layer "Mul_46" will be executed on CPU
        2023-01-10 19:24:28,454 INFO INFO: Layer "Mul_32" will be executed on CPU
        2023-01-10 19:24:28,454 INFO INFO: Layer "Mul_35" will be executed on CPU
        2023-01-10 19:24:28,454 INFO INFO: Layer "Mul_39" will be executed on CPU
        2023-01-10 19:24:28,454 INFO INFO: Layer "Mul_42" will be executed on CPU
        2023-01-10 19:24:28,454 INFO INFO: Layer "Mul_50" will be executed on CPU
        2023-01-10 19:24:28,454 INFO INFO: Layer "Mul_53" will be executed on CPU
        2023-01-10 19:24:28,454 INFO INFO: Layer "Mul_56" will be executed on CPU
        2023-01-10 19:24:28,454 INFO INFO: Layer "Mul_80" will be executed on CPU
        2023-01-10 19:24:28,454 INFO INFO: Layer "Mul_59" will be executed on CPU
        2023-01-10 19:24:28,455 INFO INFO: Layer "Mul_62" will be executed on CPU
        2023-01-10 19:24:28,455 INFO INFO: Layer "Mul_66" will be executed on CPU
        2023-01-10 19:24:28,455 INFO INFO: Layer "Mul_69" will be executed on CPU
        2023-01-10 19:24:28,455 INFO INFO: Layer "Mul_73" will be executed on CPU
        2023-01-10 19:24:28,455 INFO INFO: Layer "Mul_76" will be executed on CPU
        2023-01-10 19:24:28,455 INFO INFO: Layer "Mul_84" will be executed on CPU
        2023-01-10 19:24:28,455 INFO INFO: Layer "Mul_87" will be executed on CPU
        2023-01-10 19:24:28,455 INFO INFO: Layer "Mul_90" will be executed on CPU
        2023-01-10 19:24:28,455 INFO INFO: Layer "Mul_100" will be executed on CPU
        2023-01-10 19:24:28,455 INFO INFO: Layer "Mul_93" will be executed on CPU
        2023-01-10 19:24:28,455 INFO INFO: Layer "Mul_96" will be executed on CPU
        2023-01-10 19:24:28,455 INFO INFO: Layer "Mul_104" will be executed on CPU
        2023-01-10 19:24:28,456 INFO INFO: Layer "Mul_107" will be executed on CPU
        2023-01-10 19:24:28,456 INFO INFO: Layer "Mul_114" will be executed on CPU
        2023-01-10 19:24:28,456 INFO INFO: Layer "Mul_117" will be executed on CPU
        2023-01-10 19:24:28,456 INFO INFO: Layer "Mul_123" will be executed on CPU
        2023-01-10 19:24:28,456 INFO INFO: Layer "Mul_132" will be executed on CPU
        2023-01-10 19:24:28,456 INFO INFO: Layer "Mul_126" will be executed on CPU
        2023-01-10 19:24:28,456 INFO INFO: Layer "Mul_129" will be executed on CPU
        2023-01-10 19:24:28,456 INFO INFO: Layer "Mul_136" will be executed on CPU
        2023-01-10 19:24:28,456 INFO INFO: Layer "Mul_139" will be executed on CPU
        2023-01-10 19:24:28,456 INFO INFO: Layer "Mul_145" will be executed on CPU
        2023-01-10 19:24:28,456 INFO INFO: Layer "Mul_154" will be executed on CPU
        2023-01-10 19:24:28,456 INFO INFO: Layer "Mul_148" will be executed on CPU
        2023-01-10 19:24:28,456 INFO INFO: Layer "Mul_151" will be executed on CPU
        2023-01-10 19:24:28,457 INFO INFO: Layer "Mul_158" will be executed on CPU
        2023-01-10 19:24:28,457 INFO INFO: Layer "Mul_161" will be executed on CPU
        2023-01-10 19:24:28,457 INFO INFO: Layer "Mul_165" will be executed on CPU
        2023-01-10 19:24:28,457 INFO INFO: Layer "Mul_174" will be executed on CPU
        2023-01-10 19:24:28,457 INFO INFO: Layer "Mul_168" will be executed on CPU
        2023-01-10 19:24:28,457 INFO INFO: Layer "Mul_171" will be executed on CPU
        2023-01-10 19:24:28,457 INFO INFO: Layer "Mul_178" will be executed on CPU
        2023-01-10 19:24:28,457 INFO INFO: Layer "Mul_181" will be executed on CPU
        2023-01-10 19:24:28,457 INFO INFO: Layer "Mul_185" will be executed on CPU
        2023-01-10 19:24:28,457 INFO INFO: Layer "Mul_194" will be executed on CPU
        2023-01-10 19:24:28,457 INFO INFO: Layer "Mul_188" will be executed on CPU
        2023-01-10 19:24:28,457 INFO INFO: Layer "Mul_191" will be executed on CPU
        2023-01-10 19:24:28,457 INFO INFO: Layer "Mul_198" will be executed on CPU
        [==================================================] 100%
        2023-01-10 19:24:34,257 INFO consumed time 5.9439
        2023-01-10 19:24:34,328 WARNING Performance information does not include operators in the model running on the CPU (including HzLut whose shape is over 8192)
        2023-01-10 19:24:34,376 INFO FPS=18.71, latency = 53440.5 us   (see torch_jit_subgraph_0.html)
        2023-01-10 19:24:34,510 INFO [Tue Jan 10 19:24:34 2023] End to compile the model with march bernoulli2.
        2023-01-10 19:24:34,512 INFO The converted model node information:
        ============================================================================================================================================
        Node                                                ON   Subgraph  Type                       Cosine Similarity  Threshold                   
        ---------------------------------------------------------------------------------------------------------------------------------------------
        HZ_PREPROCESS_FOR_data                              BPU  id(0)     HzSQuantizedPreprocess     0.999625           127.000000                  
        Conv_1                                              BPU  id(0)     HzSQuantizedConv           0.998592           1.004736                    
        Mul_3                                               BPU  id(0)     HzLut                      0.998138           13.985225                   
        Conv_4                                              BPU  id(0)     HzSQuantizedConv           0.992651           13.985213                   
        Mul_6                                               BPU  id(0)     HzLut                      0.994966           16.703127                   
        Conv_7                                              BPU  id(0)     HzSQuantizedConv           0.990321           16.703127                   
        Mul_9                                               BPU  id(0)     HzLut                      0.998465           7.794779                    
        Conv_10                                             BPU  id(0)     HzSQuantizedConv           0.983401           7.791570                    
        Mul_12                                              BPU  id(0)     HzLut                      0.997777           8.028659                    
        Conv_13                                             BPU  id(0)     HzSQuantizedConv           0.991031           8.026042                    
        Mul_15                                              BPU  id(0)     HzLut                      0.992943           8.116323                    
        UNIT_CONV_FOR_Add_16                                BPU  id(0)     HzSQuantizedConv           0.995336           7.791570                    
        Conv_17                                             BPU  id(0)     HzSQuantizedConv           0.990945           16.703127                   
        Mul_19                                              BPU  id(0)     HzLut                      0.996793           17.747612                   
        ...CONV_FOR_onnx::Concat_143_0.06933_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv                                                          
        Concat_20                                           BPU  id(0)     Concat                     0.995108           8.804478                    
        Conv_21                                             BPU  id(0)     HzSQuantizedConv           0.985998           8.804478                    
        Mul_23                                              BPU  id(0)     HzLut                      0.992025           7.598925                    
        Conv_24                                             BPU  id(0)     HzSQuantizedConv           0.991117           7.595119                    
        Mul_26                                              BPU  id(0)     HzLut                      0.991777           5.766149                    
        Conv_27                                             BPU  id(0)     HzSQuantizedConv           0.994640           5.748147                    
        Mul_29                                              BPU  id(0)     HzLut                      0.996433           3.026174                    
        Conv_30                                             BPU  id(0)     HzSQuantizedConv           0.994104           2.886191                    
        Mul_32                                              BPU  id(0)     HzLut                      0.995512           4.508018                    
        Conv_33                                             BPU  id(0)     HzSQuantizedConv           0.993648           4.458879                    
        Mul_35                                              BPU  id(0)     HzLut                      0.994182           3.558093                    
        UNIT_CONV_FOR_Add_36                                BPU  id(0)     HzSQuantizedConv           0.994743           2.886191                    
        Conv_37                                             BPU  id(0)     HzSQuantizedConv           0.991709           2.473211                    
        Mul_39                                              BPU  id(0)     HzLut                      0.989208           4.479204                    
        Conv_40                                             BPU  id(0)     HzSQuantizedConv           0.992944           4.428968                    
        Mul_42                                              BPU  id(0)     HzLut                      0.994286           6.980838                    
        UNIT_CONV_FOR_Add_43                                BPU  id(0)     HzSQuantizedConv           0.995198           2.473211                    
        Conv_44                                             BPU  id(0)     HzSQuantizedConv           0.990863           5.748147                    
        Mul_46                                              BPU  id(0)     HzLut                      0.990956           4.114643                    
        ...CONV_FOR_onnx::Concat_170_0.04494_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv                                                          
        Concat_47                                           BPU  id(0)     Concat                     0.993840           5.707380                    
        Conv_48                                             BPU  id(0)     HzSQuantizedConv           0.994418           5.707380                    
        Mul_50                                              BPU  id(0)     HzLut                      0.991736           5.388514                    
        Conv_51                                             BPU  id(0)     HzSQuantizedConv           0.993635           5.364007                    
        Mul_53                                              BPU  id(0)     HzLut                      0.986075           7.765623                    
        Conv_54                                             BPU  id(0)     HzSQuantizedConv           0.996115           7.762331                    
        Mul_56                                              BPU  id(0)     HzLut                      0.990948           3.816494                    
        Conv_57                                             BPU  id(0)     HzSQuantizedConv           0.987893           3.734321                    
        Mul_59                                              BPU  id(0)     HzLut                      0.986812           5.819736                    
        Conv_60                                             BPU  id(0)     HzSQuantizedConv           0.990948           5.802512                    
        Mul_62                                              BPU  id(0)     HzLut                      0.981153           5.626144                    
        UNIT_CONV_FOR_Add_63                                BPU  id(0)     HzSQuantizedConv           0.985675           3.734321                    
        Conv_64                                             BPU  id(0)     HzSQuantizedConv           0.986720           2.895749                    
        Mul_66                                              BPU  id(0)     HzLut                      0.977147           6.111077                    
        Conv_67                                             BPU  id(0)     HzSQuantizedConv           0.978817           6.097551                    
        Mul_69                                              BPU  id(0)     HzLut                      0.974796           6.300752                    
        UNIT_CONV_FOR_Add_70                                BPU  id(0)     HzSQuantizedConv           0.978137           2.895749                    
        Conv_71                                             BPU  id(0)     HzSQuantizedConv           0.985211           4.546500                    
        Mul_73                                              BPU  id(0)     HzLut                      0.971530           6.672524                    
        Conv_74                                             BPU  id(0)     HzSQuantizedConv           0.964964           6.664093                    
        Mul_76                                              BPU  id(0)     HzLut                      0.966502           10.009397                   
        UNIT_CONV_FOR_Add_77                                BPU  id(0)     HzSQuantizedConv           0.969769           4.546500                    
        Conv_78                                             BPU  id(0)     HzSQuantizedConv           0.988043           7.762331                    
        Mul_80                                              BPU  id(0)     HzLut                      0.986741           5.253876                    
        ...CONV_FOR_onnx::Concat_204_0.03503_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv                                                          
        Concat_81                                           BPU  id(0)     Concat                     0.973960           4.448520                    
        Conv_82                                             BPU  id(0)     HzSQuantizedConv           0.987208           4.448520                    
        Mul_84                                              BPU  id(0)     HzLut                      0.973802           6.913193                    
        Conv_85                                             BPU  id(0)     HzSQuantizedConv           0.981681           6.906324                    
        Mul_87                                              BPU  id(0)     HzLut                      0.965594           9.224026                    
        Conv_88                                             BPU  id(0)     HzSQuantizedConv           0.992448           9.223116                    
        Mul_90                                              BPU  id(0)     HzLut                      0.988430           5.606626                    
        Conv_91                                             BPU  id(0)     HzSQuantizedConv           0.968618           5.586105                    
        Mul_93                                              BPU  id(0)     HzLut                      0.958150           10.471902                   
        Conv_94                                             BPU  id(0)     HzSQuantizedConv           0.969298           10.471604                   
        Mul_96                                              BPU  id(0)     HzLut                      0.964260           10.146297                   
        UNIT_CONV_FOR_Add_97                                BPU  id(0)     HzSQuantizedConv           0.964661           5.586105                    
        Conv_98                                             BPU  id(0)     HzSQuantizedConv           0.975004           9.223116                    
        Mul_100                                             BPU  id(0)     HzLut                      0.962438           9.911333                    
        ...CONV_FOR_onnx::Concat_224_0.03322_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv                                                          
        Concat_101                                          BPU  id(0)     Concat                     0.963729           4.219078                    
        Conv_102                                            BPU  id(0)     HzSQuantizedConv           0.972310           4.219078                    
        Mul_104                                             BPU  id(0)     HzLut                      0.959204           9.914267                    
        Conv_105                                            BPU  id(0)     HzSQuantizedConv           0.977106           9.913776                    
        Mul_107                                             BPU  id(0)     HzLut                      0.982392           6.799733                    
        MaxPool_108                                         BPU  id(0)     HzQuantizedMaxPool         0.993679           6.792165                    
        MaxPool_109                                         BPU  id(0)     HzQuantizedMaxPool         0.996352           6.792165                    
        MaxPool_110                                         BPU  id(0)     HzQuantizedMaxPool         0.997350           6.792165                    
        ...ONV_FOR_onnx::MaxPool_231_0.06787_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv                                                          
        ...ONV_FOR_onnx::MaxPool_232_0.06787_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv                                                          
        ...ONV_FOR_onnx::MaxPool_233_0.06787_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv                                                          
        ...CONV_FOR_onnx::Concat_234_0.06787_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv                                                          
        Concat_111                                          BPU  id(0)     Concat                     0.995251           6.792165                    
        Conv_112                                            BPU  id(0)     HzSQuantizedConv           0.988744           8.619161                    
        Mul_114                                             BPU  id(0)     HzLut                      0.972662           8.022479                    
        Conv_115                                            BPU  id(0)     HzSQuantizedConv           0.980147           8.019848                    
        Mul_117                                             BPU  id(0)     HzLut                      0.965953           8.967721                    
        Resize_119                                          BPU  id(0)     HzQuantizedResizeUpsample  0.965893           8.966578                    
        ...CONV_FOR_onnx::Concat_246_0.01916_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv                                                          
        UNIT_CONV_FOR_onnx::Conv_208_0.01916_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv                                                          
        Concat_120                                          BPU  id(0)     Concat                     0.963391           8.966578                    
        Conv_121                                            BPU  id(0)     HzSQuantizedConv           0.986149           2.433284                    
        Mul_123                                             BPU  id(0)     HzLut                      0.983297           6.423621                    
        Conv_124                                            BPU  id(0)     HzSQuantizedConv           0.979580           6.413213                    
        Mul_126                                             BPU  id(0)     HzLut                      0.976023           6.405385                    
        Conv_127                                            BPU  id(0)     HzSQuantizedConv           0.972830           6.394816                    
        Mul_129                                             BPU  id(0)     HzLut                      0.967925           7.185949                    
        Conv_130                                            BPU  id(0)     HzSQuantizedConv           0.976136           2.433284                    
        Mul_132                                             BPU  id(0)     HzLut                      0.969723           6.963424                    
        ...CONV_FOR_onnx::Concat_256_0.01522_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv                                                          
        ...CONV_FOR_onnx::Concat_259_0.01522_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv                                                          
        Concat_133                                          BPU  id(0)     Concat                     0.957710           7.180512                    
        Conv_134                                            BPU  id(0)     HzSQuantizedConv           0.954683           1.933006                    
        Mul_136                                             BPU  id(0)     HzLut                      0.945891           9.066763                    
        Conv_137                                            BPU  id(0)     HzSQuantizedConv           0.953563           9.065717                    
        Mul_139                                             BPU  id(0)     HzLut                      0.965812           7.352169                    
        Resize_141                                          BPU  id(0)     HzQuantizedResizeUpsample  0.965765           7.347457                    
        ...CONV_FOR_onnx::Concat_271_0.02880_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv                                                          
        UNIT_CONV_FOR_onnx::Conv_174_0.02880_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv                                                          
        Concat_142                                          BPU  id(0)     Concat                     0.974294           7.347457                    
        Conv_143                                            BPU  id(0)     HzSQuantizedConv           0.989032           3.657588                    
        Mul_145                                             BPU  id(0)     HzLut                      0.992494           6.087980                    
        Conv_146                                            BPU  id(0)     HzSQuantizedConv           0.989104           6.074192                    
        Mul_148                                             BPU  id(0)     HzLut                      0.992540           5.660322                    
        Conv_149                                            BPU  id(0)     HzSQuantizedConv           0.975980           5.640685                    
        Mul_151                                             BPU  id(0)     HzLut                      0.978878           9.938995                    
        Conv_152                                            BPU  id(0)     HzSQuantizedConv           0.976293           3.657588                    
        Mul_154                                             BPU  id(0)     HzLut                      0.978075           7.166039                    
        ...CONV_FOR_onnx::Concat_281_0.03712_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv                                                          
        ...CONV_FOR_onnx::Concat_284_0.03712_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv                                                          
        Concat_155                                          BPU  id(0)     Concat                     0.978210           9.938516                    
        Conv_156                                            BPU  id(0)     HzSQuantizedConv           0.944852           4.713646                    
        Mul_158                                             BPU  id(0)     HzLut                      0.956471           24.037889                   
        Conv_159                                            BPU  id(0)     HzSQuantizedConv           0.948493           24.037889                   
        Mul_161                                             BPU  id(0)     HzLut                      0.945453           7.151889                    
        ...CONV_FOR_onnx::Concat_291_0.04806_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv                                                          
        ...CONV_FOR_onnx::Resize_266_0.04806_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv                                                          
        Concat_162                                          BPU  id(0)     Concat                     0.955909           7.146291                    
        Conv_163                                            BPU  id(0)     HzSQuantizedConv           0.945652           6.103609                    
        Mul_165                                             BPU  id(0)     HzLut                      0.938230           7.221455                    
        Conv_166                                            BPU  id(0)     HzSQuantizedConv           0.962912           7.216181                    
        Mul_168                                             BPU  id(0)     HzLut                      0.956445           6.634083                    
        Conv_169                                            BPU  id(0)     HzSQuantizedConv           0.953755           6.625372                    
        Mul_171                                             BPU  id(0)     HzLut                      0.951723           10.860644                   
        Conv_172                                            BPU  id(0)     HzSQuantizedConv           0.950328           6.103609                    
        Mul_174                                             BPU  id(0)     HzLut                      0.955650           6.775457                    
        ...CONV_FOR_onnx::Concat_301_0.03780_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv                                                          
        ...CONV_FOR_onnx::Concat_304_0.03780_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv                                                          
        Concat_175                                          BPU  id(0)     Concat                     0.953305           10.860435                   
        Conv_176                                            BPU  id(0)     HzSQuantizedConv           0.929372           4.801002                    
        Mul_178                                             BPU  id(0)     HzLut                      0.941431           21.555998                   
        Conv_179                                            BPU  id(0)     HzSQuantizedConv           0.943251           21.555998                   
        Mul_181                                             BPU  id(0)     HzLut                      0.933456           8.890406                    
        ...CONV_FOR_onnx::Concat_311_0.02306_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv                                                          
        ...CONV_FOR_onnx::Resize_241_0.02306_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv                                                          
        Concat_182                                          BPU  id(0)     Concat                     0.943703           8.889181                    
        Conv_183                                            BPU  id(0)     HzSQuantizedConv           0.946935           2.928516                    
        Mul_185                                             BPU  id(0)     HzLut                      0.931021           8.757660                    
        Conv_186                                            BPU  id(0)     HzSQuantizedConv           0.937357           8.756283                    
        Mul_188                                             BPU  id(0)     HzLut                      0.918907           10.897411                   
        Conv_189                                            BPU  id(0)     HzSQuantizedConv           0.937940           10.897210                   
        Mul_191                                             BPU  id(0)     HzLut                      0.925729           12.400668                   
        Conv_192                                            BPU  id(0)     HzSQuantizedConv           0.952533           2.928516                    
        Mul_194                                             BPU  id(0)     HzLut                      0.952878           8.299829                    
        ...CONV_FOR_onnx::Concat_321_0.03825_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv                                                          
        ...CONV_FOR_onnx::Concat_324_0.03825_TO_FUSE_SCALE  BPU  id(0)     HzSQuantizedConv                                                          
        Concat_195                                          BPU  id(0)     Concat                     0.939141           12.400617                   
        Conv_196                                            BPU  id(0)     HzSQuantizedConv           0.936492           4.857968                    
        Mul_198                                             BPU  id(0)     HzLut                      0.948842           16.812071                   
        Conv_199                                            BPU  id(0)     HzSQuantizedConv           0.997939           24.037889                   
        Conv_201                                            BPU  id(0)     HzSQuantizedConv           0.998180           21.555998                   
        Conv_203                                            BPU  id(0)     HzSQuantizedConv           0.998646           16.812071
        2023-01-10 19:24:34,513 INFO [Tue Jan 10 19:24:34 2023] End to Horizon NN Model Convert.
        2023-01-10 19:24:34,587 INFO start convert to *.bin file....
        2023-01-10 19:24:34,616 INFO ONNX model output num : 3
        2023-01-10 19:24:34,621 INFO ############# model deps info #############
        2023-01-10 19:24:34,621 INFO hb_mapper version   : 1.13.3
        2023-01-10 19:24:34,621 INFO hbdk version        : 3.41.4
        2023-01-10 19:24:34,621 INFO hbdk runtime version: 3.15.7.0
        2023-01-10 19:24:34,621 INFO horizon_nn version  : 0.15.3
        2023-01-10 19:24:34,621 INFO ############# model_parameters info #############
        2023-01-10 19:24:34,621 INFO onnx_model          : /open_explorer/smart_vision/models/yolov5s-latest.onnx
        2023-01-10 19:24:34,621 INFO BPU march           : bernoulli2
        2023-01-10 19:24:34,621 INFO layer_out_dump      : False
        2023-01-10 19:24:34,621 INFO log_level           : DEBUG
        2023-01-10 19:24:34,621 INFO working dir         : /open_explorer/smart_vision/models/model_output
        2023-01-10 19:24:34,621 INFO output_model_file_prefix: yolov5s_672x672_nv12
        2023-01-10 19:24:34,621 INFO ############# input_parameters info #############
        2023-01-10 19:24:34,621 INFO ------------------------------------------
        2023-01-10 19:24:34,621 INFO ---------input info : data ---------
        2023-01-10 19:24:34,621 INFO input_name          : data
        2023-01-10 19:24:34,621 INFO input_type_rt       : nv12
        2023-01-10 19:24:34,621 INFO input_space&range   : regular
        2023-01-10 19:24:34,621 INFO input_layout_rt     : None
        2023-01-10 19:24:34,621 INFO input_type_train    : rgb
        2023-01-10 19:24:34,621 INFO input_layout_train  : NCHW
        2023-01-10 19:24:34,621 INFO norm_type           : data_scale
        2023-01-10 19:24:34,621 INFO input_shape         : 1x3x672x672
        2023-01-10 19:24:34,622 INFO scale_value         : 0.003921568627451,
        2023-01-10 19:24:34,622 INFO cal_data_dir        : /open_explorer/smart_vision/calibration_data_rgb_f32
        2023-01-10 19:24:34,622 INFO ---------input info : data end -------
        2023-01-10 19:24:34,622 INFO ------------------------------------------
        2023-01-10 19:24:34,622 INFO ############# calibration_parameters info #############
        2023-01-10 19:24:34,622 INFO preprocess_on       : False
        2023-01-10 19:24:34,622 INFO calibration_type:   : default
        2023-01-10 19:24:34,622 INFO ############# compiler_parameters info #############
        2023-01-10 19:24:34,622 INFO hbdk_pass_through_params: --O3 --core-num 1 --fast
        2023-01-10 19:24:34,622 INFO input-source        : {'data': 'pyramid', '_default_value': 'ddr'}
        2023-01-10 19:24:34,626 INFO Convert to runtime bin file sucessfully!
        2023-01-10 19:24:34,626 INFO End Model Convert
        ```
        
4. 最后使用 `04_inference.sh` 进行推断，**能够得到正确推断结果！**
    
    ![相比于v2.0模型的识别结果，能够识别靠近树梢的kite](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/e917c1e0-3563-4bdd-ad15-d679965548f9/demo.jpg)
    
    相比于v2.0模型的识别结果，能够识别靠近树梢的kite
    

# YOLOv5自定义模型训练

根据官方文档：

> The commands below reproduce YOLOv5 [COCO](https://github.com/ultralytics/yolov5/blob/master/data/scripts/get_coco.sh) results. [Models](https://github.com/ultralytics/yolov5/tree/master/models) and [datasets](https://github.com/ultralytics/yolov5/tree/master/data) download automatically from the latest YOLOv5 [release](https://github.com/ultralytics/yolov5/releases). Training times for YOLOv5n/s/m/l/x are 1/2/4/6/8 days on a V100 GPU ([Multi-GPU](https://github.com/ultralytics/yolov5/issues/475) times faster). Use the largest `--batch-size` possible, or pass `--batch-size -1` for YOLOv5 [AutoBatch](https://github.com/ultralytics/yolov5/pull/5092). Batch sizes shown for V100-16GB.
> 

```bash
python train.py --data coco.yaml --epochs 300 --weights '' --cfg yolov5n.yaml  --batch-size 128
                                                                 yolov5s                    64
                                                                 yolov5m                    40
                                                                 yolov5l                    24
                                                                 yolov5x                    16
```

使用V100基于COCO数据集训练 `yolov5s` 的批尺寸为64，时间为2天。根据GPU性能对比：[https://technical.city/en/video/GeForce-RTX-3090-vs-Tesla-V100-PCIe](https://technical.city/en/video/GeForce-RTX-3090-vs-Tesla-V100-PCIe)， 3090性能更好，显存更大（24GB vs 16GB），在服务器上进行训练的耗时或小于官方数据。

实际在实验室服务器上进行训练，需要对训练脚本输入参数进行调整。

1. 首先，如果指定 `weights` ，则会将其作为预训练权重，否则根据 `cfg` 所给定的模型结构从头开始训练。自定义模型的训练不必从头开始；
2. 可以使用 `--device 1` 特别指定使用第二个GPU；
3. 默认训练的模型结构是矩形框检测网络。需要注意的是， `--rect` 参数的含义是使用矩形（而不是默认的正方形）图像作为输入；该选项默认为 False；
https://github.com/ultralytics/yolov5/issues/2009
4. 使用默认的 `batch_size=16` ，显存使用为 5.541GB，估算在3090上可以使用的最大批量为64。

## 准备自定义数据集

[Combined Object Detection Dataset (v1, 2022-11-23 7:30am) by Y3IndividualProject](https://universe.roboflow.com/y3individualproject/combined-yizo3/dataset/1)

所得数据集文件夹中应包括一个yaml文件，其中应指定train, valid, test三组文件夹的位置。这里下载的数据集仅包含train set，故将其复制两份并分别作为 valid, test，对yaml中定义的数据集路径相应进行修改。

## 开始训练

我们已在以下软件包中实现自定义数据集训练，可参考其内容：

[](https://github.com/SOTA-Robotics/yolov5/blob/main/SOTA-README.md)

## PT模型转换为ONNX

基本流程与之前转换官方模型相同，参考上述链接。

# YOLOv5自定义模型转换

方法与部署官方模型基本类似，需要注意的是数据集不同，需识别的类别也不同，由此需要对源代码进行部分修改。我们目前已在SmartVision中实现相关代码，模型转换流程参见其README：
https://github.com/SOTA-Robotics/SmartVision

# 板端运行转换的模型

```bash
class hobot_dnn.pyeasy_dnn.TensorProperties
Parameters：
    1、tensor_type (string)：表示tensor的数据类型，例如：NV12、BGR、float32等
    2、dtype (string)：表示数据的存储类型，同numpy数据类型，例如：int8、uint8、float32等
    3、layout (string)：表示数据排布格式，NHWC或者NCHW
    4、shape (tuple)：表示存储数据的shape信息，例如：(1,3,224,224)
```

```bash
class hobot_dnn.pyeasy_dnn.pyDNNTensor
Parameters：
    1、properties (TensorProperties)：表示模型tensor的属性，详细参见 `class hobot_dnn.pyeasy_dnn.TensorProperties` 
    2、buffer (numpy)：表示模型tensor中的数据，数据访问方式同numpy
    3、name (string)：表示模型tensor的名称
```

```bash
class hobot_dnn.pyeasy_dnn.Model
Parameters：
    1、name (string)：表示模型名称
    2、inputs (tuple(pyDNNTensor))：表示模型的输入tensor信息
    3、outputs (tuple(pyDNNTensor))：表示模型的输出tensor信息
    4、forward (args &args, kwargs &kwargs)：模型推理函数接口，输入模型推理所必要的参数，返回模型推理结果
        parameters：
            args: 提供三种形式的tensor输入，详细使用参考文末示例，或者SDK的示例脚本
                非resizer模型：
                    a. numpy：单输入模型场景，直接提供numpy数据进行推理
                    b. list[numpy, numpy, ...]：多输入模型场景，将numpy数据打包成list，list长度应当为模型的输入个数
                resizer模型：
                    a. list[list[numpy, list], list[numpy, list], ...]：将numpy数据与roi框的信息打包成一个list，作为一个tensor输入，多个tensor打包成一个list，作为模型整体输入
            kwargs：core_id (int)：表示模型推理的core id，可为0,1,2，默认为0表示任意核推理。
            kwargs：priority (int)：表示当前模型推理任务的优先级，范围[0~255]，越大优先级越高。
        returns: 接口返回模型输出结果
            非resizer模型：
                a. 输出为一维tuple: tuple(pyDNNTensor)，tuple长度为模型输出个数; 
            resizer模型：
                a. 输出为二维tuple: tuple(tupe(pyDNNTensor))，len(output)长度为roi的数量，len(output[0])长度为模型单个roi输出数量。
```

[5.3. BPU 算法推理 - 旭日X3派用户手册 1.0.0 文档](https://developer.horizon.ai/api/v1/fileData/html/Python_devolep/python_dnn.html)

# 板端运行优化

[](https://developer.horizon.ai/forumDetail/136488103547258549)

## 校准数据数量对精度的影响

为验证校准数据数量对量化模型的精度是否产生影响，针对在combined数据集上训练得到的模型，分别使用不同数量的校准图片，同样在can.jpg上进行推理测试，评估数据量对量化置信度的影响（原始模型置信度为0.4798）：

| 校准图像数量 | 1 | 5 | 20 | 25 | 50 | 75 | 100-1（将原50组图片复制一份） | 100-2（互不相同，但包含原50张） | 100-3（不包含原50张） |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 量化模型置信度 | 0.4387 | 0.4739 |  | 0.4482 | 0.4438 | 0.4359 | 0.4766 | 0.4386 | 0.4462 |

![75](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/f1a2b97d-1ef3-4c5c-af54-5bd79b924bfa/demo.jpg)

75

![100-2](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/8bf8d5b3-577c-4404-921f-c4c5071ea15e/demo.jpg)

100-2

![100-3](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/73fe32cd-12b5-4c66-b2ce-097b90630872/demo.jpg)

100-3

<aside>
⚠️ 模型量化的参考图像的存放目录，图片格式支持Jpeg、Bmp等格式，输入的图片应该是使用的典型场景，一般是从测试集中选择20~100张图片，另外输入的图片要覆盖典型场景，不要是偏僻场景，如过曝光、饱和、模糊、纯黑、纯白等图片若有多个输入节点, 则应使用';'进行分隔

</aside>

<aside>
⚠️ 实验发现，在指定文件夹中放置100张以上图片，只能将其中100张转换为标定数据。

</aside>

从以上实验结果可得出初步结论：

1. 校准数据数量越大，在特定图片上取得的置信度一般越低，原因可能是要针对更多的图片调优，在模型参数上会出现摇摆。
2. 校准效果与选取的图片有关，如果与测试图片接近，则有可能取得更好的效果。
3. 在更多数据上仍能取得较好效果的模型应优先选用。

# 参考文档

[附录：开发手册](https://developer.horizon.ai/api/v1/fileData/doc/cn/source_doc/x3_ddk_docs.html)

## ISSUE

- bash: /home/clover/.local/bin/hb_mapper: 没有那个文件或目录或python版本不兼容问题。
    
    原因是没有进入到conda环境的bin执行文件夹中，需要检查bashrc文件对于PATH的设定，有可能出现在忘记设置conda的path或者多设置了.local文件的bin文件夹为PATH。