#!/usr/bin/env python3

import numpy as np
import cv2

if __name__ == '__main__':
    # 打开 usb camera: /dev/video8
    cap = cv2.VideoCapture(8)
    if(not cap.isOpened()):
        exit(-1)
    print("Open usb camera successfully")
    # 设置usb camera的输出图像格式为 MJPEG， 分辨率 1920 x 1080
    codec = cv2.VideoWriter_fourcc( 'M', 'J', 'P', 'G' )
    cap.set(cv2.CAP_PROP_FOURCC, codec)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    _ ,frame = cap.read()

    # print(frame.shape)

    if frame is None:
        print("Failed to get image from usb camera")
    
    cv2.imwrite("imf.jpg", frame)
