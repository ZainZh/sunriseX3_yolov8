from hobot_spdev import libsppydev as srcampy
import cv2
from src.tools.common import nv12_2_bgr_opencv
import time
from src.yolov8.YOLOv8 import YOLOv8BIN
import numpy as np

## reference:
# https://developer.horizon.ai/api/v1/fileData/documents_pi/Python_Develop/40pin_user_guide.html


class MipiCamera(object):
    def __init__(self):
        self.camera = srcampy.Camera()
        ret = self.camera.open_cam(-1, [[512, 512]])
        # ret = self.camera.open_cam(video_index,[width, height])
        if ret != 0:
            raise RuntimeError("Open camera failed")
        # self.open_camera()

    # def open_camera(self, video_index: int = 0, width: int = 1920, height: int = 1080):
    #     """
    #     open camera and set parameters
    #     Args:
    #
    #         video_index: The index of the camera device.
    #         fps: The frame rate of the camera.
    #         width: The width of the camera image.
    #         height: The height of the camera image.
    #
    #     Returns:
    #
    #     """
    #     # ret = self.camera.open_vps([1920, 1080], [640, 640])
    #     ret = self.camera.open_cam(-1, [[1920, 1080], [512, 512], [1920, 1080]])
    #     # ret = self.camera.open_cam(video_index,[width, height])
    #     if ret != 0:
    #         raise RuntimeError("Open camera failed")

    def get_frame(self, width: int, height: int, module: int = 2, ):
        """
        get image from camera
        Returns: image

        """
        return self.camera.get_frame(module, [width, height])

    def get_frame_bgr(self, width: int, height: int, module: int = 2, ):
        """
        get image from camera
        Returns: image

        """
        nv12_img = self.camera.get_frame(module, [width, height])
        bgr_img = nv12_2_bgr_opencv(nv12_img, height, width)
        return bgr_img
    def close(self):
        self.camera.close()

if __name__ == "__main__":
    camera = MipiCamera()
    model_path = "../../model_output/horizon_ultra.bin"
    yolov8_detector = YOLOv8BIN(model_path)
    # img = camera.get_frame_bgr(512,512)
    img =cv2.imread("../../images/test/18.jpg")
    boxes, scores, class_ids = yolov8_detector(img)
    print(class_ids)
    combined_img = yolov8_detector.draw_detections(img)

    cv2.imwrite("detected_objects.jpg", combined_img)
    cv2.imwrite("test.png", img)

    print("a")
