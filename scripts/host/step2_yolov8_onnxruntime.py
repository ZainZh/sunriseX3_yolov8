import cv2


from src.yolov8.YOLOv8 import YOLOv8ONNX


if __name__ == '__main__':
    # Initialize yolov8 object detector
    # model_path = "/home/clover/Downloads/yolov8x.onnx"
    model_path = "/home/clover/ultralytics/runs/detect/train6/weights/best.onnx"
    yolov8_detector = YOLOv8ONNX(model_path, conf_thres=0.2, iou_thres=0.3)


    img = cv2.imread("../../images/test/100.jpg")

    # Detect Objects
    boxes, scores, class_ids = yolov8_detector(img)
    # Draw detections
    combined_img = yolov8_detector.draw_detections(img)
    cv2.imwrite("../../images/onnx_detected.jpg", combined_img)
    # cv2.waitKey(0)
