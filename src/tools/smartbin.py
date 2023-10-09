import rospy
import json
import importlib
import importlib.util

import os.path as osp
from src.tools.modbus_control import ModbusController
from src.tools.common import load_omega_config
from src.yolov8.YOLOv8 import YOLOv8BIN
from hobot_spdev import libsppydev as srcampy

__all__ = ["SmartBin"]


class SortingModuleHandle(object):
    def __init__(self, sorting_module_config_name):
        """Initializer of the SortingModuleHandle.

        Args:
            sorting_module_config_name (str): Name of the YAML configuration file for the SortingModule.
        """
        self.config = load_omega_config(sorting_module_config_name)
        self.modbus_address = self.config["modbus_address"]
        self.modbus_band_rate = self.config["modbus_band_rate"]
        self.modbus_timeout = self.config["modbus_timeout"]
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
        rospy.sleep(0.1)
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
                self.model_config["model_path"],
                self.model_config["onf_thres"],
                self.model_config["iou_thres"],
            )
        else:
            self.model = None

        self._round_flag = 0
        self._camera = srcampy.Camera()
        self._segmentation_loop = rospy.Timer(
            rospy.Duration.from_sec(0.2), self._task_callback
        )

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
        for robot_handle in self._robot_handles:
            robot_handle.update_encoder_values()

        rgb_image = self._camera.grab()
        if rgb_image is None:
            camera_connect_status = self.usb_devices.check_devices("camera")
            self._camera = camera_self_healing(self._camera, camera_connect_status)
            rgb_image = self._camera.grab()

        grasp_info_list = self._segmentation_server.get_grasp_info_list(rgb_image)
        if not grasp_info_list:
            return None

        return grasp_info_list

    def _print_grasp_info(self, grasp_info_list):
        """Prints the number of objects detected in this round and the number of each type of objects detected."""
        print_info(
            f"Round {self._round_flag} | Detected {len(grasp_info_list)} new items |"
        )
        if not grasp_info_list:
            print_info("---------------------------------------------------------")
            return
        for label in self.all_classes:
            label_count = sum(1 for info in grasp_info_list if info.label == label)
            if label_count > 0:
                print_info("Class: {}, item num {}".format(label, label_count))
        print_info("---------------------------------------------------------")

    def _do_segmentation(self):
        """This function first calls the segmentation service to provide the GraspInfo list.
        Then it filter the grasps already known in the last round and processes only new objects to grasp.

        Returns:
            None
        """
        grasp_info_list = self._call_segmentation_service()
        if grasp_info_list is None:
            return

        # In theory, all absolute encoder values read by robot encoders should be the same,
        # so here we use the reading from the first robot's encoder.
        if not self._system_test:
            filtered_grasp_info_list = self._item_filter.select_new_instances(
                grasp_info_list, self._robot_handles[0].absolute_encoder_value
            )
        else:
            filtered_grasp_info_list = grasp_info_list
        self._print_grasp_info(filtered_grasp_info_list)

        for grasp_info in filtered_grasp_info_list:
            # assert isinstance(grasp_info, GraspInfo)
            for robot_handle in self._robot_handles:
                if robot_handle.try_to_grasp(grasp_info):
                    self._grasp_counts[grasp_info.label] += 1
                    # The break makes sure that the object is processed by only one robot
                    break

    def _publish_grasp_counts(self):
        """Publishes counts for grasping the objects with a String type ROS msg whose content is in JSON format.

        Returns:
            None
        """
        grasp_counts_json = json.dumps(self._grasp_counts)
        self._grasp_counts_publisher.publish(String(grasp_counts_json))

    def _task_callback(self, event):
        """Main callback function for executing the task."""
        prediction_results = self._do_segmentation()
        sorting_module_index = self.post_process(prediction_results)
        self.sorting_module.execute(sorting_module_index)
        self._round_flag += 1
        if rospy.is_shutdown():
            self._camera.close()
