import cv2


from yolov8 import YOLOv8,YOLOv8ONNX,YOLOv8BIN


if __name__ == '__main__':
    # Initialize yolov8 object detector
    model_path = "/home/clover/Downloads/yolov8x.onnx"
    yolov8_detector = YOLOv8ONNX(model_path, conf_thres=0.2, iou_thres=0.3)


    img = cv2.imread("/home/clover/Downloads/coco128/images/train2017/test2.jpg")

    # Detect Objects
    boxes, scores, class_ids = yolov8_detector(img)
    # Draw detections
    combined_img = yolov8_detector.draw_detections(img)
    cv2.namedWindow("Detected Objects", cv2.WINDOW_NORMAL)
    cv2.imshow("Detected Objects", combined_img)
    cv2.imwrite("doc/img/detected_objects.jpg", combined_img)
    cv2.waitKey(0)
