import cv2


from yolov8 import YOLOv8ONNX


if __name__ == '__main__':
    # Initialize yolov8 object detector
    model_path = "/opt/hobot/model/rdkultra/basic/yolov8x.onnx"
    yolov8_detector = YOLOv8ONNX(model_path, conf_thres=0.4, iou_thres=0.65)

    img = cv2.imread("kite.jpg")

    # Detect Objects
    boxes, scores, class_ids = yolov8_detector(img)
    # Draw detections
    combined_img = yolov8_detector.draw_detections(img)

    cv2.imwrite("detected_objects.jpg", combined_img)

