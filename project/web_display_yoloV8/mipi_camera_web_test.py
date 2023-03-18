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


def postprocess(model_output,
                model_hw_shape,
                origin_image=None,
                origin_img_shape=None,
                score_threshold=0.5,
                nms_threshold=0.6,
                dump_image=False):
    input_height = model_hw_shape[0]
    input_width = model_hw_shape[1]
    if origin_image is not None:
        origin_image_shape = origin_image.shape[0:2]
    else:
        origin_image_shape = origin_img_shape

    prediction_bbox = decode(outputs=model_output,
                             score_threshold=score_threshold,
                             origin_shape=origin_image_shape,
                             input_size=512)

    prediction_bbox = nms(prediction_bbox, iou_threshold=nms_threshold)

    prediction_bbox = np.array(prediction_bbox)
    topk = min(prediction_bbox.shape[0], 1000)

    if topk != 0:
        idx = np.argpartition(prediction_bbox[..., 4], -topk)[-topk:]
        prediction_bbox = prediction_bbox[idx]

    if dump_image and origin_image is not None:
        draw_bboxs(origin_image, prediction_bbox)
    return prediction_bbox


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def softmax(x, axis=-1):
    e_x = np.exp(x - np.max(x, axis=axis, keepdims=True))
    y = e_x / e_x.sum(axis=axis, keepdims=True)
    return y


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

    BBOXES = list()
    strides = [8, 16, 32, 64, 128]
    # print("len of outputs,", len(outputs))
    dfl = np.arange(0, 16, dtype=np.float32)
    results = []
    for i in range(len(outputs) // 2):
        bboxes_feat = outputs[i * 2 + 0]
        scores_feat = sigmoid(outputs[i * 2 + 1])
        Argmax = scores_feat.argmax(-1)
        Max = scores_feat.max(-1)
        indices = np.where(Max > 0.4)
        hIdx, wIdx = indices
        num_proposal = hIdx.size
        if not num_proposal:
            continue
        assert scores_feat.shape[-1] == 4
        scores = Max[hIdx, wIdx]
        bboxes = bboxes_feat[hIdx, wIdx].reshape(-1, 4, 16)
        bboxes = softmax(bboxes, -1) @ dfl
        argmax = Argmax[hIdx, wIdx]

        for k in range(num_proposal):
            x0, y0, x1, y1 = bboxes[k]
            score = scores[k]
            clsid = argmax[k]
            print(clsid, " clsid")
            h, w, stride = hIdx[k], wIdx[k], 1 << (i + 3)
            x0 = ((w + 0.5 - x0) * stride - 1) * 1
            y0 = ((h + 0.5 - y0) * stride - 1) * 1
            x1 = ((w + 0.5 + x1) * stride - 1) * 1
            y1 = ((h + 0.5 + y1) * stride - 1) * 1
            # clip
            x0 = min(max(x0, 0), 1)
            y0 = min(max(y0, 0), 1)
            x1 = min(max(x1, 0), 1)
            y1 = min(max(y1, 0), 1)

            pred_bbox = np.concatenate(
                [np.array([x0, y0, x1 - x0, y1 - y0]), np.array([float(score)]), np.array([clsid])], dtype=np.float32)
            index = pred_bbox[..., 4] > score_threshold
            pred_bbox = pred_bbox[index]
            BBOXES.append(pred_bbox)

    return np.concatenate(BBOXES)


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
cam.open_cam(0, 1, fps, [640, 1920], [640, 1080])
enc = srcampy.Encoder()
enc.encode(0, 3, 1920, 1080)
classes = get_classes()


async def web_service(websocket, path):
    while True:
        FrameMessage = x3_pb2.FrameMessage()
        FrameMessage.img_.height_ = 1080
        FrameMessage.img_.width_ = 1920
        FrameMessage.img_.type_ = "JPEG"

        img = cam.get_img(2, 640, 640)
        img = np.frombuffer(img, dtype=np.uint8)
        outputs = models[0].forward(img)
        if not outputs:
            print("no outputs")
            continue
        outputs = [o.buffer[0] for o in outputs]
        # Do post process
        prediction_bbox = postprocess(outputs, input_shape, origin_img_shape=(1080, 1920))

        print("the shape of prediction_bbox is ", np.shape(prediction_bbox))
        origin_image = cam.get_img(2, 1920, 1080)
        enc.encode_file(origin_image)
        FrameMessage.img_.buf_ = enc.get_img()
        FrameMessage.smart_msg_.timestamp_ = int(time.time())

        prot_buf = serialize(FrameMessage, prediction_bbox)

        await websocket.send(prot_buf)
    cam.close_cam()


if __name__ == '__main__':
    start_server = websockets.serve(web_service, "0.0.0.0", 8080)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()