# 导入 YOLOv8
from ultralytics import YOLO

# 载入预训练权重
model = YOLO("best.pt")

# 指定 opset=11 并且使用 onnx-sim 简化 ONNX
success = model.export(format="onnx", opset=11, simplify=True)
