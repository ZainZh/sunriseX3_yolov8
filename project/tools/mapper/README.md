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
