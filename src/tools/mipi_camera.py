from hobot_spdev import libsppydev as srcampy
import cv2

import time
## reference:
# https://developer.horizon.ai/api/v1/fileData/documents_pi/Python_Develop/40pin_user_guide.html


class MipiCamera(object):
    def __init__(self):
        self.camera = srcampy.Camera()
        self.open_camera()

    def open_camera(self,  video_index: int = -1, width: int = 1920, height: int = 1080):
        """
        open camera and set parameters
        Args:

            video_index: The index of the camera device.
            fps: The frame rate of the camera.
            width: The width of the camera image.
            height: The height of the camera image.

        Returns:

        """
        ret = self.camera.open_vps([1920, 1080], [640, 640])
        # ret = self.camera.open_cam(video_index,[width, height])
        if ret != 0:
            raise RuntimeError("Open camera failed")

    def get_frame(self, width: int, height: int, module: int = 2, ):
        """
        get image from camera
        Returns: image

        """
        return self.camera.get_frame(module, [width, height])

if __name__ == "__main__":
    camera = MipiCamera()
    img = camera.get_frame(1920, 1080)
    cv2.imwrite("test.png", img)

    print("a")