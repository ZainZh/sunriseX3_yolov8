#!/usr/bin/env python3
import cv2
from src.yolov5.YOLOv5 import YOLOv5BIN




if __name__ == "__main__":
    # models = dnn.load("/opt/hobot/model/rdkultra/basic/yolov5s_672x672_nv12.bin")
    models_path = "../../model_output/horizon_ultra.bin"

    yolov5_detector = YOLOv5BIN(models_path)

    img = cv2.imread("../../images/test/37.jpg")

    boxes, scores, class_ids = yolov5_detector(img)

    combined_img = yolov5_detector.draw_detections(img)

    cv2.imwrite("detected_objects.jpg", combined_img)