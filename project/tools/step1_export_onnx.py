# 导入 YOLOv8
import click
from ultralytics import YOLO


def print_help():
    ctx = click.get_current_context()
    click.echo(ctx.get_help())
    ctx.exit()


@click.command()
@click.option(
    "--model_path",
    default="best.pt",
    help="Path of the trained 'pt' type model that you want to transform to the 'onnx' type.",
)
def main(model_path):
    # 载入预训练权重
    model = YOLO(model_path)
    # 指定 opset=11 并且使用 onnx-sim 简化 ONNX
    success = model.export(format="onnx", opset=11, simplify=True)


if __name__ == "__main__":
    main()
