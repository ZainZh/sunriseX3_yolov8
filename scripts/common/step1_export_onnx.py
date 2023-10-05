# 导入 YOLOv8
import click
from ultralytics import YOLO
from src.common import print_info, print_error, print_help
import os.path as osp


@click.command()
@click.option(
    "--model_path",
    help="Path of the trained 'pt' type model that you want to transform to the 'onnx' type.",
)
def main(model_path):
    if not model_path or not osp.exists(model_path):
        print_help()
        print_error(f"Path '{model_path}' is not valid, exit.")
        exit(-1)
    # 载入预训练权重
    model = YOLO(model_path)
    # 指定 opset=11 并且使用 onnx-sim 简化 ONNX
    success = model.export(format="onnx", opset=11, simplify=True)
    if success:
        print_info("The 'onnx' model is stored in the same path as the 'pt' model.")
    else:
        print_error("Export fail! Please check your model.")


if __name__ == "__main__":
    main()
