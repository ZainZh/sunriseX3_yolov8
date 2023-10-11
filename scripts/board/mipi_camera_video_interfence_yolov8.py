# !/usr/bin/env python3
import sys
import signal
import os
import numpy as np
import cv2
import colorsys
from time import time, sleep
import multiprocessing
from threading import BoundedSemaphore
# Camera API libs

from hobot_spdev import libsppydev as srcampy
from hobot_dnn import pyeasy_dnn as dnn
import threading
from src.yolov8.YOLOv8 import YOLOv8BIN

from src.tools.common import nv12_2_bgr_opencv

image_counter = None
is_running = 1


## reference:
# https://developer.horizon.ai/api/v1/fileData/documents_pi/Python_Develop/python_vio.html#camera
def signal_handler(signal, frame):
    global is_running
    is_running = 0


def get_display_res():
    if os.path.exists("/usr/bin/get_hdmi_res") == False:
        return 1920, 1080

    import subprocess
    p = subprocess.Popen(["/usr/bin/get_hdmi_res"], stdout=subprocess.PIPE)
    result = p.communicate()
    res = result[0].split(b',')
    res[1] = max(min(int(res[1]), 1920), 0)
    res[0] = max(min(int(res[0]), 1080), 0)
    return int(res[1]), int(res[0])


disp_w, disp_h = get_display_res()


# detection model class names
def get_classes():
    return np.array([
        "bottle", "can",
    ])


def get_hw(pro):
    if pro.layout == "NCHW":
        return pro.shape[2], pro.shape[3]
    else:
        return pro.shape[1], pro.shape[2]


def postprocess(model_output, score_threshold=0.5, nms_threshold=0.6):
    origin_img_shape = (disp_h, disp_w)
    prediction_bbox = decode(outputs=model_output,
                             score_threshold=score_threshold,
                             origin_shape=origin_img_shape,
                             input_size=512)
    prediction_bbox = nms(prediction_bbox, iou_threshold=nms_threshold)
    prediction_bbox = np.array(prediction_bbox)
    topk = min(prediction_bbox.shape[0], 1000)

    if topk != 0:
        idx = np.argpartition(prediction_bbox[..., 4], -topk)[-topk:]
        prediction_bbox = prediction_bbox[idx]

    return prediction_bbox


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
        cls = outputs[i]
        bbox = outputs[i + 5]
        ce = outputs[i + 10]
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


def print_properties(pro):
    print("tensor type:", pro.tensor_type)
    print("data type:", pro.dtype)
    print("layout:", pro.layout)
    print("shape:", pro.shape)


class ParallelExector(object):
    def __init__(self, counter, parallel_num=4):
        global image_counter
        image_counter = counter
        self.parallel_num = parallel_num
        if parallel_num != 1:
            self._pool = multiprocessing.Pool(processes=self.parallel_num,
                                              maxtasksperchild=5)
            self.workers = BoundedSemaphore(self.parallel_num)

    def infer(self, bbox, score, class_id):
        if self.parallel_num == 1:
            run(bbox, score, class_id)
        else:
            self.workers.acquire()
            self._pool.apply_async(func=run,
                                   args=(bbox, score, class_id,),
                                   callback=self.task_done,
                                   error_callback=print)

    def task_done(self, *args, **kwargs):
        """Called once task is done, releases the queue is blocked."""
        self.workers.release()

    def close(self):
        if hasattr(self, "_pool"):
            self._pool.close()
            self._pool.join()


def limit_display_cord(coor):
    coor[0] = max(min(disp_w, coor[0]), 0)
    # min coor is set to 2 not 0, leaving room for string display
    coor[1] = max(min(disp_h, coor[1]), 2)
    coor[2] = max(min(disp_w, coor[2]), 0)
    coor[3] = max(min(disp_h, coor[3]), 0)
    return coor


def run(bboxes, scores, class_ids):
    global image_counter
    # Do post process
    for index, bbox in enumerate(bboxes):
        # get bbox coordinates
        coor = np.array(bbox[:4], dtype=np.int32)
        coor = limit_display_cord(coor)

        # get bbox score
        score = float(bbox[4])

        # get bbox name
        box_class_index = int(bbox[5])
        box_class_name = classes[box_class_index]

        # concat bbox string
        bbox_string = '%s: %.2f' % (box_class_name, score)
        bbox_string = bbox_string.encode('gb2312')

        # concat bbox color
        box_color = colors[box_class_index]
        color_base = 0xFF000000
        box_color_ARGB = color_base | (box_color[0]) << 16 | (
            box_color[1]) << 8 | (box_color[2])

        print("{} is in the picture with confidence:{:.4f}, bbox:{}".format(
            box_class_name, score, coor))

        # if new frame come in, need to flush the display buffer.
        # For the meaning of parameters, please refer to the relevant documents of display api
        if index == 0:
            disp.set_rect(coor[0], coor[1], coor[2], coor[3], 1,
                          box_color_ARGB)
            disp.set_word(coor[0], coor[1] - 2, bbox_string, 1,
                          box_color_ARGB)
        else:
            disp.set_rect(coor[0], coor[1], coor[2], coor[3], 0,
                          box_color_ARGB)
            disp.set_word(coor[0], coor[1] - 2, bbox_string, 0,
                          box_color_ARGB)

    # fps timer and counter
    box_draw_finish_time = time()
    with image_counter.get_lock():
        image_counter.value += 1
    if image_counter.value == 100:
        finish_time = time()
        print(
            f"Total time cost for 100 frames: {finish_time - start_time}, fps: {100 / (finish_time - start_time)}"
        )


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    model_path = "../../model_output/horizon_ultra.bin"
    yolov8_detector = YOLOv8BIN(model_path, conf_thres=0.4, iou_thres=0.3)

    # Camera API, get camera object
    cam = srcampy.Camera()

    # get model info

    # Open f37 camera
    # For the meaning of parameters, please refer to the relevant documents of camera
    a = cam.open_cam(-1, [[1920, 1080]])
    if a != 0:
        raise RuntimeError("Open camera failed")
    # Get HDMI display object
    disp = srcampy.Display()
    # For the meaning of parameters, please refer to the relevant documents of HDMI display
    disp.display([disp_w, disp_h])

    # bind camera directly to display
    srcampy.bind(cam, disp)

    # change disp for bbox display
    # disp.display([disp_w, disp_h])

    # setup for box color and box string
    classes = get_classes()
    num_classes = len(classes)
    hsv_tuples = [(1.0 * x / num_classes, 1., 1.) for x in range(num_classes)]
    colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
    colors = list(
        map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)),
            colors))

    # fps timer and counter
    start_time = time()
    image_counter = multiprocessing.Value("i", 0)

    # post process parallel executor
    parallel_exe = ParallelExector(image_counter)

    while is_running:
        try:
            cam_start_time = time()
            img = cam.get_frame(2, [1920, 1080])
            img = nv12_2_bgr_opencv(img, 1080, 1920)
            cam_finish_time = time()

            if img is None:
                print("img is null")
                pass
            else:
                buffer_start_time = time()
                boxes, scores, class_ids = yolov8_detector(img)
                infer_finish_time = time()
                parallel_exe.infer(boxes, scores, class_ids)

        except Exception as e:
            parallel_exe.close()
            srcampy.unbind(cam, disp)
            cam.close()
            disp.close()
            exit(e)
    parallel_exe.close()
    srcampy.unbind(cam, disp)
    cam.close()
    disp.close()
