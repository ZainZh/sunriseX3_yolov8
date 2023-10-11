
import json
import importlib
import importlib.util

import os.path as osp
import time

from src.tools.modbus_control import ModbusController
from src.tools.common import load_omega_config,print_info,camera_self_healing
from src.tools.data_types import DetectionOutput
from src.yolov8.YOLOv8 import YOLOv8BIN
# from src.tools.mvsdk import Camera
from src.tools.mipi_camera import MipiCamera as Camera

__all__ = ["SmartBin"]


class SortingModuleHandle(object):
    def __init__(self, sorting_module_config_name):
        """Initializer of the SortingModuleHandle.

        Args:
            sorting_module_config_name (str): Name of the YAML configuration file for the SortingModule.
        """
        self.config = load_omega_config(sorting_module_config_name)
        self.modbus_address = self.config["modbus_address"]
        self.modbus_band_rate = self.config["modbus_baud_rate"]
        self.modbus_timeout = self.config["execution_timeout"]
        self.sorting_module = ModbusController(
            address=self.modbus_address,
            baud_rate=self.modbus_band_rate,
            timeout=self.modbus_timeout,
        )

    def execute(self, sorting_module_index: int):
        """Executes the sorting module.

        Args:
            sorting_module_index (int): The index of the sorting module to execute.
        """
        # Turn on the sorting module
        self.sorting_module.write_coil(sorting_module_index, True)
        time.sleep(0.1)
        # Turn off the sorting module
        self.sorting_module.write_coil(sorting_module_index, False)



class SmartBin(object):
    def __init__(self, config_name="smartbin"):
        """Initializer of the TaskManager.

        Args:
            config_name (str): Name of the YAML configuration file for the TaskManager.
        """
        self.config = load_omega_config(config_name)
        self.model_structure = self.config["model_structure"]
        try:
            self.model_config = load_omega_config(self.model_structure)
        except:
            # TODO: Add support for other models
            raise ValueError(
                "Unsupported model structure: {}. \n Support: 'YOLOv8'".format(
                    self.model_structure
                )
            )

        if self.model_structure == "YOLOv8":
            self.model = YOLOv8BIN(
                self.config["model_path"],
                self.model_config["onf_thres"],
                self.model_config["iou_thres"],
            )
        else:
            self.model = None

        self._round_flag = 0
        self._camera = Camera()
        # self.sorting_module = SortingModuleHandle("sorting_module")
        while True:
            self._task_callback()

    def __del__(self):
        if self._camera:
            self._camera.close()

    def _call_segmentation_service(self):
        """This function first get instant and absolute encoder values, then grab the RGB image, and finally calls the
        segmentation service with the image to get a list of GraspInfo.

        Returns:
            None if no valid grasps are detected.
            GraspInfoCollection if valid grasps are detected.
        """

        rgb_image = self._camera.get_frame_bgr(width=1920, height=1080)
        if rgb_image is None:
            self._camera = camera_self_healing(self._camera)
            rgb_image = self._camera.grab()

        boxes, scores, labels = self.model(rgb_image)
        if boxes is []:
            return None
        print("bbox:", boxes, "scores:", scores, "labels:", labels)
        return boxes, scores, labels

    def _do_detection(self):
        """This function first calls the segmentation service to provide the GraspInfo list.
        Then it filter the grasps already known in the last round and processes only new objects to grasp.

        Returns:
            None
        """
        bboxes, scores, labels = self._call_segmentation_service()

        return DetectionOutput(bboxes, scores, labels)

    @staticmethod
    def post_process(detection_output: DetectionOutput):
        """
        This function takes the detection output and returns the index of the sorting module to execute.
        Args:
            detection_output:

        Returns:

        """
        sorting_module_index = 0
        return sorting_module_index

    def _task_callback(self):
        """Main callback function for executing the task."""
        detection_output= self._do_detection()
        sorting_module_index = self.post_process(detection_output)
        # self.sorting_module.execute(sorting_module_index)
        self._round_flag += 1
