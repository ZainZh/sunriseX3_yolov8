# !/usr/bin/env python
from __future__ import print_function

import time
from datetime import datetime

import os
import cv2
import numpy as np

import src.tools.mvsdk.mvsdk as mvsdk

from src.tools.common import print_info, print_error


class Camera(object):
    def __init__(self, device_info, exposure_time=15, img_size=(720, 1280)):
        super(Camera, self).__init__()
        self.device_info = device_info
        self._camera_handle = 0
        self._capabilities = None
        self._frame_buffer = 0
        self.exposure_time = exposure_time
        self.img_size = img_size
        self.h, self.w = self.img_size[0], self.img_size[1]

    def open(self, config_name="mighty_nachi"):
        if self._camera_handle > 0:
            return True

        try:
            camera_handle = mvsdk.CameraInit(self.device_info, -1, -1)
        except mvsdk.CameraException as e:
            print_error("CameraInit Failed({}): {}".format(e.error_code, e.message))
            return False

        # read config
        current_path = os.path.abspath(__file__)
        config_path = os.path.join(
            os.path.dirname(current_path), f"Camera/Config/{config_name}.Config"
        )
        mvsdk.CameraReadParameterFromFile(camera_handle, config_path)
        # set roi
        max_width = 2448
        max_height = 2048
        width = 2100
        height = width * self.h // self.w  # [1400, 2100]
        offset_y, offset_x = (max_height - height) // 2, (max_width - width) // 2
        # if config_name == "mighty":
        #     self._set_camera_resolution(
        #         camera_handle, offset_x, offset_y, width, height
        #     )

        # 获取相机特性描述
        camera_capabilities = mvsdk.CameraGetCapability(camera_handle)

        # 判断是黑白相机还是彩色相机
        monoCamera = camera_capabilities.sIspCapacity.bMonoSensor != 0

        # 黑白相机让ISP直接输出MONO数据，而不是扩展成R=G=B的24位灰度
        if monoCamera:
            mvsdk.CameraSetIspOutFormat(camera_handle, mvsdk.CAMERA_MEDIA_TYPE_MONO8)
        else:
            mvsdk.CameraSetIspOutFormat(camera_handle, mvsdk.CAMERA_MEDIA_TYPE_BGR8)

        # 计算RGB buffer所需的大小，这里直接按照相机的最大分辨率来分配
        frame_buffer_size = (
            camera_capabilities.sResolutionRange.iWidthMax
            * camera_capabilities.sResolutionRange.iHeightMax
            * (1 if monoCamera else 3)
        )

        # 分配RGB buffer，用来存放ISP输出的图像
        # 备注：从相机传输到PC端的是RAW数据，在PC端通过软件ISP转为RGB数据（如果是黑白相机就不需要转换格式，但是ISP还有其它处理，所以也需要分配这个buffer）
        frame_buffer = mvsdk.CameraAlignMalloc(frame_buffer_size, 16)

        # 相机模式切换成连续采集
        mvsdk.CameraSetTriggerMode(camera_handle, 0)

        # 手动曝光，曝光时间30ms
        # mvsdk.CameraSetAeState(camera_handle, 0)
        # mvsdk.CameraSetExposureTime(camera_handle,  self.exposure_time * 1000)
        # auto
        # mvsdk.CameraSetAeState(camera_handle, 1)
        # mvsdk.CameraSetAeTarget(camera_handle, 120)
        # mvsdk.CameraSetAeExposureRange(camera_handle, 0, 15 * 1000)
        # mvsdk.CameraSetGamma(camera_handle, 70)
        # mvsdk.CameraSetContrast(camera_handle, 100)
        # mvsdk.CameraSetSaturation(camera_handle, 110)
        # mvsdk.CameraSetWbMode(camera_handle, True)

        target = mvsdk.CameraGetAeTarget(camera_handle)
        exp_value = mvsdk.CameraGetAeExposureRange(camera_handle)
        exp_time = mvsdk.CameraGetExposureTime(camera_handle)
        print_info(
            f"Target is {target}, exp_value is {exp_value}, exp_time is {exp_time}"
        )
        lut_mode = mvsdk.CameraGetLutMode(camera_handle)
        gamma = mvsdk.CameraGetGamma(camera_handle)
        contrast = mvsdk.CameraGetContrast(camera_handle)
        saturation = mvsdk.CameraGetSaturation(camera_handle)
        color_temp = mvsdk.CameraGetPresetClrTemp(camera_handle)
        position = mvsdk.CameraGetWbWindow(camera_handle)
        print_info(
            f"lut mode is {lut_mode}, gamma is {gamma}, contrast is {contrast}, "
            f"saturation is {saturation}, color_temp is {color_temp}, pos is {position}"
        )

        # 让SDK内部取图线程开始工作
        mvsdk.CameraPlay(camera_handle)

        self._camera_handle = camera_handle
        self._frame_buffer = frame_buffer
        self._capabilities = camera_capabilities
        return True

    @staticmethod
    def _set_camera_resolution(hCamera, offset_x, offset_y, width, height):
        sRoiResolution = mvsdk.tSdkImageResolution()
        sRoiResolution.iIndex = 0xFF
        sRoiResolution.iWidth = width
        sRoiResolution.iWidthFOV = width
        sRoiResolution.iHeight = height
        sRoiResolution.iHeightFOV = height
        sRoiResolution.iHOffsetFOV = offset_x
        sRoiResolution.iVOffsetFOV = offset_y
        sRoiResolution.iWidthZoomSw = 0
        sRoiResolution.iHeightZoomSw = 0
        sRoiResolution.uBinAverageMode = 0
        sRoiResolution.uBinSumMode = 0
        sRoiResolution.uResampleMask = 0
        sRoiResolution.uSkipMode = 0
        return mvsdk.CameraSetImageResolution(hCamera, sRoiResolution)

    def close(self):
        if self._camera_handle > 0:
            mvsdk.CameraUnInit(self._camera_handle)
            self._camera_handle = 0

        mvsdk.CameraAlignFree(self._frame_buffer)
        self._frame_buffer = 0

    def grab_bgr(self):
        # 从相机取一帧图片
        hCamera = self._camera_handle
        pFrameBuffer = self._frame_buffer
        try:
            pRawData, frame_head = mvsdk.CameraGetImageBuffer(hCamera, 200)
            mvsdk.CameraImageProcess(hCamera, pRawData, pFrameBuffer, frame_head)
            mvsdk.CameraReleaseImageBuffer(hCamera, pRawData)

            # 此时图片已经存储在pFrameBuffer中，对于彩色相机pFrameBuffer=RGB数据，黑白相机pFrameBuffer=8位灰度数据
            # 把pFrameBuffer转换成opencv的图像格式以进行后续算法处理
            frame_data = (mvsdk.c_ubyte * frame_head.uBytes).from_address(pFrameBuffer)
            frame = np.frombuffer(frame_data, dtype=np.uint8)
            frame = frame.reshape(
                (
                    frame_head.iHeight,
                    frame_head.iWidth,
                    1 if frame_head.uiMediaType == mvsdk.CAMERA_MEDIA_TYPE_MONO8 else 3,
                )
            )
            return cv2.resize(
                frame, (self.w, self.h), interpolation=cv2.INTER_LINEAR
            ).astype(np.uint8)
        except mvsdk.CameraException as e:
            if e.error_code != mvsdk.CAMERA_STATUS_TIME_OUT:
                print(
                    "CameraGetImageBuffer failed({}): {}".format(
                        e.error_code, e.message
                    )
                )
            return None

    def grab(self):
        bgr = self.grab_bgr()
        if bgr is not None:
            return bgr
        else:
            return None

    @classmethod
    def init_camera(cls, config_name="mighty"):
        """Initialize the camera.

        Returns:
            The Camera instance.

        Raises:
            RuntimeError If no camera available.
        """
        device_list = mvsdk.CameraEnumerateDevice()
        if not device_list:
            raise RuntimeError("No camera was found")

        camera = cls(device_list[0], exposure_time=14, img_size=[720, 1280])
        for i, device_info in enumerate(device_list):
            print(
                "{}: {} {}".format(
                    i, device_info.GetFriendlyName(), device_info.GetPortType()
                )
            )
        if camera.open(config_name):
            print_info("Camera opened")
            return camera
        raise RuntimeError("Failed to open the camera")

    @classmethod
    def reconnect_camera(cls, config_name="mighty"):
        """Reconnect the camera

        Returns:
            camera:The Camera instance.
        """
        device_list = mvsdk.CameraEnumerateDevice()
        if not device_list:
            return None
        camera = cls(device_list[0], exposure_time=14, img_size=[720, 1280])
        if camera.open(config_name) and (camera.grab() is not None):
            print_info("Successfully reconnect the camera")
            return camera
        return None


def main_loop():
    # 枚举相机
    DevList = mvsdk.CameraEnumerateDevice()
    nDev = len(DevList)
    if nDev < 1:
        print("No camera was found!")
        return

    for i, DevInfo in enumerate(DevList):
        print("{}: {} {}".format(i, DevInfo.GetFriendlyName(), DevInfo.GetPortType()))

    cams = []
    cam = Camera(DevList[0])
    if cam.open():
        cams.append(cam)
    win_name = cam.device_info.GetFriendlyName()
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
    num = 0
    while (cv2.waitKey(1) & 0xFF) != ord("q"):
        for cam in cams:
            # tic = time.time()
            frame = cam.grab()
            if frame is not None:
                # max 2448 # iHeight:2048, 3
                # frame = cv2.resize(frame[:, :, ::-1], (1280, 720), interpolation=cv2.INTER_LINEAR)
                frame = frame[:, :, ::-1]
                cv2.imshow(win_name, frame)
                if cv2.waitKey(1) & 0xFF == ord("s"):
                    cv2.imwrite(
                        f"{os.path.expanduser('~')}/Pictures/mvsdk_images/opencv_save_images/"
                        f"{datetime.now().strftime('%d%m%Y_%H%M%S')}.png",
                        frame,
                    )

    for cam in cams:
        cam.close()


def main():
    try:
        main_loop()
    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
