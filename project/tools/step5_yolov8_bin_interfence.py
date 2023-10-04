import cv2


from yolov8 import YOLOv8BIN


if __name__ == '__main__':
    # Initialize yolov8 object detector
    model_path = "/opt/hobot/model/rdkultra/basic/yolov8n_672x672_nv12.bin"
    yolov8_detector = YOLOv8BIN(model_path, conf_thres=0.2, iou_thres=0.3)

    img = cv2.imread(".kite.jpg")

    # Detect Objects
    boxes, scores, class_ids = yolov8_detector(img)
    # Draw detections
    combined_img = yolov8_detector.draw_detections(img)
    cv2.namedWindow("Detected Objects", cv2.WINDOW_NORMAL)
    cv2.imshow("Detected Objects", combined_img)
    cv2.imwrite("doc/img/detected_objects.jpg", combined_img)
    cv2.waitKey(0)
