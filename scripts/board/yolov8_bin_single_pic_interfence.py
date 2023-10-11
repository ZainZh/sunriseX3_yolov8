import cv2
from src.yolov8.YOLOv8 import YOLOv8BIN



if __name__ == '__main__':
    # Initialize yolov8 object detector
    model_path = "../../model_output/horizon_ultra.bin"
    yolov8_detector = YOLOv8BIN(model_path, conf_thres=0.4, iou_thres=0.3)

    img = cv2.imread("../../images/test/1.jpg")

    # Detect Objects
    boxes, scores, class_ids = yolov8_detector(img)
    # Draw detections
    combined_img = yolov8_detector.draw_detections(img)

    cv2.imwrite("detected_objects.jpg", combined_img)

