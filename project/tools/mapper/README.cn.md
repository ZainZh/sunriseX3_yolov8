# Yolov5s

## 准备模型和数据
1. YOLOv5s模型
  1.1 可以从URL: https://github.com/ultralytics/yolov5/releases/tag/v2.0 中下载相应的pt文件
  1.2 验证 md5sum: 
  2e296b5e31bf1e1b6b8ea4bf36153ea5  yolov5l.pt
  16150e35f707a2f07e7528b89c032308  yolov5m.pt
  42c681cf466c549ff5ecfe86bcc491a0  yolov5s.pt
  069a6baa2a741dec8a2d44a9083b6d6e  yolov5x.pt
  1.3 下载完成后通过脚本https://github.com/ultralytics/yolov5/blob/v2.0/models/export.py 进行pt文件到onnx文件的转换
  1.4 对于 YOLOv5 模型，我们在模型结构上的修改点主要在于几个输出节点处。由于目前的浮点转换工具链暂时不支持 5 维的 Reshape，所以我们在 prototxt中进行了删除，并将其移至后处理中执行。同时我们还添加了一个 transpose 算子，使该节点将以 NHWC 进行输出。这是因为在地平线芯片中， BPU 硬件本身以 NHWC 的layout 运行，这样修改后可以让 BPU 直接输出结果，而不在量化模型中引入额外的transpose。 详情请见文档中benchmark部分的图文介绍
2. COCO验证集，用于计算模型精度，可以从COCO官网下载：http://cocodataset.org/
3. 校准数据集：可以从COCO验证集中抽取50张图片作为校准数据
4. 原始浮点模型精度：`[IoU=0.50:0.95] 0.352 [IoU=0.50] 0.542`

# Yolov5s

## Prepare model and data
1. YOLOv5s model
  1.1 corresponding pt file can be downloaded from URL: https://github.com/ultralytics/yolov5/releases/tag/v2.0
  1.2 verification md5sum: 
  2e296b5e31bf1e1b6b8ea4bf36153ea5  yolov5l.pt
  16150e35f707a2f07e7528b89c032308  yolov5m.pt
  42c681cf466c549ff5ecfe86bcc491a0  yolov5s.pt
  069a6baa2a741dec8a2d44a9083b6d6e  yolov5x.pt
  1.3 after download, convert pt file into ONNX file using the `https://github.com/ultralytics/yolov5/blob/v2.0/models/export.py` script
  1.4 As for YOLOv5 model, in terms of model structure, we modified some output nodes. As currently OpenExplorer XJ3 Toolchain doesn't support 5-dimensional Reshape, we deleted it in the prototxt and moved it to post-process. Meanwhile, we've aslo added a transpose operator to enable the node to dump NHWC. This is because in Horizon's ASIC, BPU hardware runs NHWC layout, therefore, BPU can directly dump results after some modifications, rather than introducing additional transpose in quantized model. For more details please refer to the text and table in the Benchmark section.
2. COCO verification dataset is used for computing model accuracy and can be downloaded from COCO official website: http://cocodataset.org/
3. Calibration dataset: extract 50 images from COCO verification dataset to serve as calibration dataset
4. origin float model accuracy : `[IoU=0.50:0.95] 0.352 [IoU=0.50] 0.542`
