import numpy as np
import click
import time
import cv2
from omegaconf import OmegaConf
import os.path as osp
def _preprocess_print(*args):
    """Preprocess the input for colorful printing.

    Args:
        args: Any/None One or more any type arguments to print.

    Returns:
        str Msg to print.
    """
    str_args = ""
    for a in args:
        if isinstance(a, np.ndarray):
            str_args += "\n" + np.array2string(a, separator=", ")
        else:
            str_args += " " + str(a)
    separate_with_newline = str_args.split("\n")
    extra_whitespaces_removed = []
    for b in separate_with_newline:
        extra_whitespaces_removed.append(" ".join(b.split()))
    return "\n".join(extra_whitespaces_removed)


def print_debug(*args):
    """Print information with green."""
    print("".join(["\033[1m\033[92m", _preprocess_print(*args), "\033[0m"]))


def print_info(*args):
    """Print information with sky blue."""
    print("".join(["\033[1m\033[94m", _preprocess_print(*args), "\033[0m"]))


def print_warning(*args):
    """Print a warning with yellow."""
    print("".join(["\033[1m\033[93m", _preprocess_print(*args), "\033[0m"]))


def print_error(*args):
    """Print error with red."""
    print("".join(["\033[1m\033[91m", _preprocess_print(*args), "\033[0m"]))


def print_help():
    ctx = click.get_current_context()
    click.echo(ctx.get_help())
    ctx.exit()

def bgr2nv12_opencv(image):
    height, width = image.shape[0], image.shape[1]
    area = height * width
    yuv420p = cv2.cvtColor(image, cv2.COLOR_BGR2YUV_I420).reshape((area * 3 // 2,))
    y = yuv420p[:area]
    uv_planar = yuv420p[area:].reshape((2, area // 4))
    uv_packed = uv_planar.transpose((1, 0)).reshape((area // 2,))

    nv12 = np.zeros_like(yuv420p)
    nv12[:height * width] = y
    nv12[height * width:] = uv_packed
    return nv12

def load_omega_config(config_name):
    """Load the configs listed in config_name.yaml.

    Args:
        config_name (str): Name of the config file.

    Returns:
        (dict): A dict of configs.
    """
    return OmegaConf.load(
        osp.join(osp.dirname(__file__), "../../config/{}.yaml".format(config_name))
    )

def camera_self_healing(camera, camera_connect_status = True):
    """

    Args:
        camera: The Camera instance.
        camera_connect_status: bool If true, the camera will be considered as connected with the USB port.

    Returns:
        _camera: The Camera instance.
    """
    from src.tools.mvsdk import Camera

    if camera_connect_status:
        print_info("camera reconnecting...")
        for _ in range(5):
            camera.close()
            _camera = Camera.reconnect_camera()
            if _camera is not None:
                return _camera
            else:
                print_info("Failed to reconnect, try again.")
                time.sleep(1)
        return None

    else:
        raise RuntimeError("Failed to reconnect the camera, check the USB connector.")