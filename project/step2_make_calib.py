from pathlib import Path
import cv2
import numpy as np
from numpy import ndarray
from typing import List, Tuple, Union
import random


def letterbox(
        im: ndarray,
        new_shape: Union[Tuple, List] = (640, 640),
        color: Union[Tuple, List] = (114, 114, 114)
) -> Tuple[ndarray, float, Tuple[float, float]]:
    # Resize and pad image while meeting stride-multiple constraints
    shape = im.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])

    # Compute padding
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[
        1]  # wh padding

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    if shape[::-1] != new_unpad:  # resize
        im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    im = cv2.copyMakeBorder(im,
                            top,
                            bottom,
                            left,
                            right,
                            cv2.BORDER_CONSTANT,
                            value=color)  # add border
    return im, r, (dw, dh)


def blob(im: ndarray) -> ndarray:
    im = im.transpose([2, 0, 1])  # hwc -> chw
    im = np.ascontiguousarray(im)
    return im


if __name__ == '__main__':
    path = Path('./coco128')
    save = Path('./calib_f32')
    cnt = 0
    all_dirs = [i for i in path.iterdir()]
    random.shuffle(all_dirs)
    for i in all_dirs:
        if cnt >= 50:
            break
        img = cv2.imread(str(i))
        img = letterbox(img)[0]
        img = blob(img[:, :, ::-1])  # bgr -> rgb
        print(img.shape)
        img.astype(np.float32).tofile(str(save / (i.stem + '.rgbchw')))
        cnt += 1
