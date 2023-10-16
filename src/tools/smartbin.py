import json
import importlib
import importlib.util

import os.path as osp
import os
import time
import cv2
from src.tools.modbus_control import ModbusController
from src.tools.common import (
    load_omega_config,
    print_info,
    camera_self_healing,
    nv12_2_bgr_opencv,
    timeit,
)
from src.tools.data_types import DetectionOutput
from src.yolov8.YOLOv8 import YOLOv8BIN

# from src.tools.mvsdk import Camera
from src.tools.mipi_camera import MipiCamera as Camera
from datetime import datetime

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

    def execute(self, sorting_module_list: list):
        """Executes the sorting module.

        Args:
            sorting_module_list (int): The index of the sorting module to execute.
        """
        # Turn on the sorting module
        for sorting_module_index in sorting_module_list:
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
            self.model = YOLOv8BIN(self.config["model_path"])
        else:
            self.model = None
        self._round_flag = 0
        self._camera = Camera()
        self.class_names = self.model_config["class_names"]
        self.sorting_module = SortingModuleHandle("sorting_module")
        self._save_path = "../../images/output"
        self._labeled_image_dir = osp.join(self._save_path, "labeled")
        if not osp.exists(self._labeled_image_dir):
            os.makedirs(self._labeled_image_dir)
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
        nv12_image = self._camera.get_frame(width=512, height=512)
        # warm-up camera
        if self._round_flag <= 10:
            return [], [], []
        if nv12_image is None:
            self._camera = camera_self_healing(self._camera)
            nv12_image = self._camera.get_frame(width=512, height=512)
        # self.draw_detections(nv12_image)
        boxes, scores, labels = self.model(nv12_image)
        if len(boxes) == 0:
            return [], [], []
        # self.draw_detections(nv12_image)
        class_name = []
        for label in labels:
            class_name.append(self.class_names[int(label)])
        print_info("bbox:", boxes, "scores:", scores, "labels:", class_name)
        return boxes, scores, labels

    def draw_detections(self, nv12_image):
        """

        Args:
            nv12_image:

        Returns:

        """
        bgr_image = nv12_2_bgr_opencv(nv12_image, 512, 512)
        draw_image = self.model.draw_detections(bgr_image)
        name_prefix = "{}".format(datetime.now().strftime("%H%M%S%f")[:-3])
        bbox_image_name = "{}_bbox.png".format(name_prefix)
        cv2.imwrite(osp.join(self._labeled_image_dir, bbox_image_name), draw_image)

    @timeit
    def _do_detection(self):
        """This function first calls the segmentation service to provide the GraspInfo list.
        Then it filter the grasps already known in the last round and processes only new objects to grasp.

        Returns:
            None
        """
        bboxes, scores, labels = self._call_segmentation_service()

        return DetectionOutput(bboxes, scores, labels)

    def post_process(self,detection_outputs: DetectionOutput):
        """
        This function takes the detection output and returns the index of the sorting module to execute.
        Args:
            detection_outputs:

        Returns:

        """
        sorting_module_list = []
        for i, [label, bbox, _] in enumerate(detection_outputs):
            sorting_module_index = int(5 - bbox.center.x // (512 / 6))
            print("label:", label, "index:", sorting_module_index)
            if (self.class_names[int(label)] == "bottle" and sorting_module_index in [3, 4, 5]) or (
                self.class_names[int(label)] == "can" and sorting_module_index in [0, 1, 2]
            ):
                print_info("index:", sorting_module_index)
                if sorting_module_index == 5:
                    sorting_module_index =4
                sorting_module_list.append(sorting_module_index)
        return sorting_module_list

    def _task_callback(self):
        """Main callback function for executing the task."""
        detection_output = self._do_detection()
        if len(detection_output) != 0:
            sorting_module_index = self.post_process(detection_output)
            self.sorting_module.execute(sorting_module_index)
            for i in range(15):
                nv12_image = self._camera.get_frame(width=512, height=512)
        self._round_flag += 1
