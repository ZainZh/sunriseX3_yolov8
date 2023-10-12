#!/usr/bin/env python3

import cv2
from src.yolov5.utils import postprocess
from src.tools.common import bgr2nv12_opencv
from hobot_dnn import pyeasy_dnn as dnn
import time


def get_hw(pro):
    if pro.layout == "NCHW":
        return pro.shape[2], pro.shape[3]
    else:
        return pro.shape[1], pro.shape[2]


def print_properties(pro):
    print("tensor type:", pro.tensor_type)
    print("data type:", pro.dtype)
    print("layout:", pro.layout)
    print("shape:", pro.shape)


if __name__ == "__main__":
    # models = dnn.load("/opt/hobot/model/rdkultra/basic/yolov5s_672x672_nv12.bin")
    models = dnn.load("../../model_output/horizon_ultra.bin")
    # 打印输入 tensor 的属性
    print_properties(models[0].inputs[0].properties)
    # 打印输出 tensor 的属性
    print(len(models[0].outputs))
    for output in models[0].outputs:
        print_properties(output.properties)

    img_file = cv2.imread("../../images/kite.jpg")
    time1 = time.time()
    h, w = get_hw(models[0].inputs[0].properties)
    des_dim = (w, h)
    resized_data = cv2.resize(img_file, des_dim, interpolation=cv2.INTER_AREA)
    nv12_data = bgr2nv12_opencv(resized_data)
    time2 = time.time()
    outputs = models[0].forward(nv12_data)
    time3 = time.time()
    prediction_bbox = postprocess(
        outputs, model_hw_shape=(672, 672), origin_image=img_file
    )
    time4 = time.time()
    print("pre_process:", time2 - time1)
    print("predict:", time3 - time2)
    print("post_process:", time4 - time3)

    print(prediction_bbox)
