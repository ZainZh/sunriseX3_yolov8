from hobot_spdev import libsppydev as srcampy
import cv2
from src.tools.common import nv12_2_bgr_opencv, load_omega_config
import time
from src.yolov8.YOLOv8 import YOLOv8BIN
import numpy as np
from src.yolov8.utils import draw_detections

## reference:
# https://developer.horizon.ai/api/v1/fileData/documents_pi/Python_Develop/40pin_user_guide.html


class MipiCamera(object):
    def __init__(self, config_name="mipicamera"):
        self.camera = srcampy.Camera()
        self.config = load_omega_config(config_name)
        self.input_height = self.config["input_height"]
        self.input_width = self.config["input_width"]
        ret = self.camera.open_cam(-1, [[self.input_width, self.input_height]])
        # ret = self.camera.open_cam(video_index,[width, height])
        if ret != 0:
            raise RuntimeError("Open camera failed")
        # self.open_camera()


    def get_frame(self, width: int, height: int, module: int = 2, ):
        """
        get image from camera
        Returns: image

        """
        return np.frombuffer(self.camera.get_frame(module, [width, height]), dtype=np.uint8)

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

    def __del__(self):
        if self.camera:
            self.camera.close()

if __name__ == "__main__":
    camera = MipiCamera()
    # model_path = "/opt/hobot/model/rdkultra/basic/yolov8n_512x512_nv12.bin"
    # yolov8_detector = YOLOv8BIN(model_path)
    # img = camera.get_frame(512,512)
    # # img =cv2.imread("../../images/test/18.jpg")
    # boxes, scores, class_ids = yolov8_detector(img)
    # print("boxes", boxes)
    # print(class_ids)
    # bgr_img = nv12_2_bgr_opencv(img, 512,512)
    # combined_img = yolov8_detector.draw_detections(bgr_img)
    #
    n=0
    while n<5:
        img = camera.get_frame_bgr(512,512)
        cv2.imwrite(f"test1_{n}.png", img)
        n+=1
    # img = camera.get_frame_bgr(1024,1024)
    # # cv2.imwrite("detected_objects.jpg", combined_img)
    # cv2.imwrite("test.png", img)
    #
    # print("a")
