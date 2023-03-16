import asyncio
import os
import time

import cv2
import numpy as np
import websockets
from hobot_dnn import pyeasy_dnn
# Camera API libs
from hobot_vio import libsrcampy as srcampy

import x3_pb2
from step4_inference import nms as yolov8_nms
from step4_inference import postprocess as pre_postprocess
from step4_inference import ratioresize

fps = 30


# detection model class names
def get_classes():
    return np.array(['Can', 'Glass-Drink', 'paper', 'pet bottle'])


def bgr2nv12_opencv(image):
    height, width = image.shape[0], image.shape[1]
    area = height * width
    yuv420p = cv2.cvtColor(image, cv2.COLOR_RGB2YUV_I420).reshape((area * 3 // 2,))
    y = yuv420p[:area]
    uv_planar = yuv420p[area:].reshape((2, area // 4))
    uv_packed = uv_planar.transpose((1, 0)).reshape((area // 2,))

    nv12 = np.zeros_like(yuv420p)
    nv12[:height * width] = y
    nv12[height * width:] = uv_packed
    return nv12


def get_hw(pro):
    if pro.layout == "NCHW":
        return pro.shape[2], pro.shape[3]
    else:
        return pro.shape[1], pro.shape[2]


def decode(outputs, score_threshold, origin_shape, input_size=512):
    def _distance2bbox(points, distance):
        x1 = points[..., 0] - distance[..., 0]
        y1 = points[..., 1] - distance[..., 1]
        x2 = points[..., 0] + distance[..., 2]
        y2 = points[..., 1] + distance[..., 3]
        return np.stack([x1, y1, x2, y2], -1)

    def _scores(cls, ce):
        cls = 1 / (1 + np.exp(-cls))
        ce = 1 / (1 + np.exp(-ce))
        return np.sqrt(ce * cls)

    def _bbox(bbox, stride, origin_shape, input_size):
        h, w = bbox.shape[1:3]
        yv, xv = np.meshgrid(np.arange(h), np.arange(w))
        xy = (np.stack((yv, xv), 2) + 0.5) * stride
        bbox = _distance2bbox(xy, bbox)
        # opencv read, shape[1] is w, shape[0] is h
        scale_w = origin_shape[1] / input_size
        scale_h = origin_shape[0] / input_size
        scale = max(origin_shape[0], origin_shape[1]) / input_size
        # origin img is pad resized
        # bbox = bbox * scale
        # origin img is resized
        bbox = bbox * [scale_w, scale_h, scale_w, scale_h]
        return bbox

    bboxes = list()
    strides = [8, 16, 32, 64, 128]

    for i in range(len(strides)):
        cls = outputs[i].buffer
        bbox = outputs[i + 5].buffer
        ce = outputs[i + 10].buffer
        scores = _scores(cls, ce)

        classes = np.argmax(scores, axis=-1)
        classes = np.reshape(classes, [-1, 1])
        max_score = np.max(scores, axis=-1)
        max_score = np.reshape(max_score, [-1, 1])
        bbox = _bbox(bbox, strides[i], origin_shape, input_size)
        bbox = np.reshape(bbox, [-1, 4])

        pred_bbox = np.concatenate([bbox, max_score, classes], axis=1)

        index = pred_bbox[..., 4] > score_threshold
        pred_bbox = pred_bbox[index]
        bboxes.append(pred_bbox)

    return np.concatenate(bboxes)


def nms(bboxes, iou_threshold, sigma=0.3, method='nms'):
    def bboxes_iou(boxes1, boxes2):
        boxes1 = np.array(boxes1)
        boxes2 = np.array(boxes2)
        boxes1_area = (boxes1[..., 2] - boxes1[..., 0]) * \
                      (boxes1[..., 3] - boxes1[..., 1])
        boxes2_area = (boxes2[..., 2] - boxes2[..., 0]) * \
                      (boxes2[..., 3] - boxes2[..., 1])
        left_up = np.maximum(boxes1[..., :2], boxes2[..., :2])
        right_down = np.minimum(boxes1[..., 2:], boxes2[..., 2:])
        inter_section = np.maximum(right_down - left_up, 0.0)
        inter_area = inter_section[..., 0] * inter_section[..., 1]
        union_area = boxes1_area + boxes2_area - inter_area
        ious = np.maximum(1.0 * inter_area / union_area,
                          np.finfo(np.float32).eps)

        return ious

    classes_in_img = list(set(bboxes[:, 5]))
    best_bboxes = []

    for cls in classes_in_img:
        cls_mask = (bboxes[:, 5] == cls)
        cls_bboxes = bboxes[cls_mask]

        while len(cls_bboxes) > 0:
            max_ind = np.argmax(cls_bboxes[:, 4])
            best_bbox = cls_bboxes[max_ind]
            best_bboxes.append(best_bbox)
            cls_bboxes = np.concatenate(
                [cls_bboxes[:max_ind], cls_bboxes[max_ind + 1:]])
            iou = bboxes_iou(best_bbox[np.newaxis, :4], cls_bboxes[:, :4])
            weight = np.ones((len(iou),), dtype=np.float32)

            assert method in ['nms', 'soft-nms']

            if method == 'nms':
                iou_mask = iou > iou_threshold
                weight[iou_mask] = 0.0
            if method == 'soft-nms':
                weight = np.exp(-(1.0 * iou ** 2 / sigma))

            cls_bboxes[:, 4] = cls_bboxes[:, 4] * weight
            score_mask = cls_bboxes[:, 4] > 0.
            cls_bboxes = cls_bboxes[score_mask]

    return best_bboxes


def serialize(FrameMessage, prediction_bbox):
    if (prediction_bbox.shape[0] > 0):
        for i in range(prediction_bbox.shape[0]):
            # get class name
            Target = x3_pb2.Target()
            id = int(prediction_bbox[i][5])
            print(classes[id])
            Target.type_ = classes[id]
            Box = x3_pb2.Box()
            Box.type_ = classes[id]
            Box.score_ = prediction_bbox[i][4]

            Box.top_left_.x_ = prediction_bbox[i][0]
            Box.top_left_.y_ = prediction_bbox[i][1]
            Box.bottom_right_.x_ = prediction_bbox[i][2]
            Box.bottom_right_.y_ = prediction_bbox[i][3]

            Target.boxes_.append(Box)
            FrameMessage.smart_msg_.targets_.append(Target)
    prot_buf = FrameMessage.SerializeToString()
    return prot_buf


def sensor_reset_shell():
    os.system("echo 19 > /sys/class/gpio/export")
    os.system("echo out > /sys/class/gpio/gpio19/direction")
    os.system("echo 0 > /sys/class/gpio/gpio19/value")
    time.sleep(0.2)
    os.system("echo 1 > /sys/class/gpio/gpio19/value")
    os.system("echo 19 > /sys/class/gpio/unexport")
    os.system("echo 1 > /sys/class/vps/mipi_host0/param/stop_check_instart")


sensor_reset_shell()
models = pyeasy_dnn.load('../models/yolov8n_smartbin.bin')
input_shape = (640, 640)
cam = srcampy.Camera()
cam.open_cam(0, 1, fps, [640, 640], [640, 640])
enc = srcampy.Encoder()
enc.encode(0, 3, 640, 640)
classes = get_classes()

score_thres = 0.8
iou_thres = 0.65
num_classes = 4


async def web_service(websocket, path):
    while True:
        FrameMessage = x3_pb2.FrameMessage()
        FrameMessage.img_.height_ = 640
        FrameMessage.img_.width_ = 640
        FrameMessage.img_.type_ = "JPEG"

        img = cam.get_img(2, 640, 640)
        img = np.frombuffer(img, dtype=np.uint8)
        outputs = models[0].forward(img)
        if not outputs[0]:
            print("no outputs")
            continue
        outputs = [o.buffer[0] for o in outputs]
        # Do post process
        prediction_bboxes = pre_postprocess(outputs, score_thres, iou_thres, 640,
                                  640, dh=1, dw=1, ratio_h=1, ratio_w=1, reg_max=16,
                                  num_classes=4)
        prediction_bboxes = yolov8_nms(*prediction_bboxes)

        print("the shape of results", np.shape(prediction_bboxes))
        prediction_bboxes = np.array(prediction_bboxes)

        origin_image = cam.get_img(2, 640, 640)
        enc.encode_file(origin_image)
        FrameMessage.img_.buf_ = enc.get_img()
        FrameMessage.smart_msg_.timestamp_ = int(time.time())

        prot_buf = serialize(FrameMessage, prediction_bboxes)

        await websocket.send(prot_buf)
    cam.close_cam()


if __name__ == '__main__':
    start_server = websockets.serve(web_service, "0.0.0.0", 8080)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
