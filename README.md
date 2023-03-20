# sunriseX3_yolov8

- [sunriseX3\_yolov8](#sunrisex3_yolov8)
  - [前序开发板与开发机配置](#前序开发板与开发机配置)
  - [模型转换操作思路](#模型转换操作思路)
  - [操作步骤](#操作步骤)
    - [训练模型](#训练模型)
    - [导出onnx模型，bin模型](#导出onnx模型bin模型)
      - [快速使用](#快速使用)
      - [手动调整最新commit](#手动调整最新commit)
    - [对导出的模型进行测试](#对导出的模型进行测试)
    - [板载运行测试](#板载运行测试)
      - [静态监测](#静态监测)
      - [实时跟踪监测](#实时跟踪监测)

旭日x3派是[地平线公司](https://developer.horizon.ai/sunrise)推出的嵌入式边缘计算板，接口兼容树莓派，具有5Tops端侧推理与4核ARM A53处理能力。可同时多路Camera Sensor的输入并支持H.264/H.265编解码。
为了实现轻量化模型部署，以满足对一些小型设备对物体识别的要求。在yolo系列开发者[tripleMu](https://github.com/triple-Mu)的帮助下，实现了将最新框架yolov8的最新版本自定义训练模型部署到旭日x3派上进行运行。同时实现了yolov8模型下的mipi摄像头静态监测与实时检测，为后续连接末端执行器并实现控制打下基础。
本文配套工具在ubuntu18.04与20.04下经过了运行测试。

## 前序开发板与开发机配置

关于开发板上运行环境的设置与开发机开发环境的设置参考该[SETUP](./SETUP.md)文档进行配置。


## 模型转换操作思路

根据网络上的教程和讨论，发现在pytorch训练得到pt模型后转为onnx模型的过程中，Detect类中的forward函数中，会对得到的预测结果进行进行后处理封装（封装成一个整体的result数据结构），同时由于X3派中支持的模型结构为`NHWC`结构，而pytorch训练得到的模型为`NCHW`结构，所以提前对forward函数中得到的模型结构进行Transpose转换，避免在板中运行时进行不必要的计算，拖慢计算速度。总结一下，在通过最新yoloV8，pytorch训练框架得到.pt训练模型后，需要在转换onnx模型和板载运行bin模型之前，对源代码中的modules.py文件 Detect类下的 forward函数进行如下两个处理，来提升板载运行效率及兼容性：

- 去掉forward函数中在得到预测result后对于result的后处理。
- 在forward函数中得到预测result后, 对于结果进行Transpose处理，把`NCHW`结构的模型提前转换为`NHWC`结构。

## 操作步骤

### 训练模型

1. 创建虚拟python环境yoloV8，并进入安装依赖项

```bash
python3.8 -m venv $HOME/.yolov8 --clear
source $HOME/.yolov8/bin/activate
pip install -r requirements.txt
```

根据yoloV8最新文档，代码，准备数据集正常进行模型训练。

❗ATTENTION:将yoloV8的环境安装在我们第一步创建的.yoloV8环境中，便于我们后续更改源码后对其进行处理。

根据[YoloV8](https://github.com/ultralytics/ultralytics)官方文档及训练方式进行训练。

本步目标：得到yoloV8训练框架训练得到的后缀为.pt的模型。

### 导出onnx模型，bin模型

在得到正常训练框架训练得到的.pt后缀模型后，本步骤最终要将其转换为X3计算板可以运行的.bin后缀模型，为了实现这一目标，我们要先将其转换为中间步骤的.onnx模型。

而在导出onnx模型之前，因为计算板所需模型结构和yoloV8导出的默认模型结构不同，要根据前述思路来对源码进行更改。同时由于yoloV8库还处于不断更新中，所以我们提供了根据当时最新的commit的更改作为submodules附在[ultralytics](ultralytics)文件夹中，可直接根据更改好的内容进行操作。同时，也将具体更改步骤描述如下，以防未来yoloV8增加了新的特性。
#### 快速使用
1. 卸载原虚拟环境中的yoloV8库——ultralytics

```bash
source $HOME/.yolov8/bin/activate
pip uninstall ultralytics
```
2. 进入utralytics库重新安装已更改好的代码依赖库

```bash
cd ultralytics
python setup.py install
```

3. 导出onnx模型

```bash
cd ../project/tools
python step1_export_onnx.py --model_path best.pt
```
#### 手动调整最新commit
具体操作如下

1. 卸载原虚拟环境中的yoloV8库——ultralytics

```bash
source $HOME/.yolov8/bin/activate
pip uninstall ultralytics
```

2. 进入最新拉取的yoloV8源码位置，对modules.py源码进行更改

```bash
cd {ultralytics's location}/ultralytics/nn
```

3. 更改modules.py中Detect类中forward函数，并重新安装yoloV8环境。

```bash
## 原来的代码
def forward(self, x):
        shape = x[0].shape  # BCHW
        for i in range(self.nl):
            x[i] = torch.cat((self.cv2[i](x[i]), self.cv3[i](x[i])), 1)
        if self.training:
            return x
        elif self.dynamic or self.shape != shape:
            self.anchors, self.strides = (x.transpose(0, 1) for x in make_anchors(x, self.stride, 0.5))
            self.shape = shape

        if self.export and self.format == 'edgetpu':  # FlexSplitV ops issue
            x_cat = torch.cat([xi.view(shape[0], self.no, -1) for xi in x], 2)
            box = x_cat[:, :self.reg_max * 4]
            cls = x_cat[:, self.reg_max * 4:]
        else:
            box, cls = torch.cat([xi.view(shape[0], self.no, -1) for xi in x], 2).split((self.reg_max * 4, self.nc), 1)
        dbox = dist2bbox(self.dfl(box), self.anchors.unsqueeze(0), xywh=True, dim=1) * self.strides
        y = torch.cat((dbox, cls.sigmoid()), 1)
        return y if self.export else (y, x)
```

```bash
## 将上面的函数替换为如下的代码
def forward(self, x):
        res = []
        for i in range(self.nl):
            bboxes = self.cv2[i](x[i]).permute(0, 2, 3, 1)
            scores = self.cv3[i](x[i]).permute(0, 2, 3, 1)
            res.append(bboxes)
            res.append(scores)
        return tuple(res)
```

```bash
## 安装modified的yoloV8环境，这步会将上述更改好的code打包成api在环境中。
source $HOME/.yolov8/bin/activate
cd {ultralytics's location}
python setup.py install
```

4. 导出onnx模型

```bash
cd ../project/tools
python step1_export_onnx.py --model_path best.pt
```

### 对导出的模型进行测试

运行代码库（bpu_yolov8）中onnxruntime-infer.py文件，对得到的.onnx文件进行检查，因为在板载上，.bin模型的预测处理方式和.onnx模型的预测处理方式是一致的，两者之间在代码层面只存在读取模型方面的差异，所以如果onnx文件的检查没有问题，在板载运行上一般也问题不大。

正常情况下，该步会对训练集的一些图片进行试预测，如果可以正常在画面上输出预测后的图像，则证明.onnx模型的转换没有问题。则可以对其进行.bin后缀模型的导出。

```bash
bash step3_convert_bin.sh
```

### 板载运行测试

将转换好的bin模型和代码库通过云端拷贝到X3运行板上，进行运行测试

#### 静态监测

#### 实时跟踪监测