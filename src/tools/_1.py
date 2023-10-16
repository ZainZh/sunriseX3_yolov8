import rospy
import json
import importlib
import importlib.util

import os.path as osp
import numpy as np

from mighty_tools.devices import Conveyor, UsbDevices
from mighty_tools.mvsdk import Camera
from mighty_tools.common import (
    load_omega_config,
    omega_to_list,
    print_info,
    print_warning,
    camera_self_healing,
)

from std_msgs.msg import String

from mighty_tools.data_types import GraspInfo
from mighty_tools.SegmentationServer import SegmentationServer

__all__ = ["TaskManager"]


class ItemFilter(object):
    def __init__(self, config_name):
        """Construct a filter for selecting newly detected items and prevent sending the same object multiple times for
        the robot to grasp.

        Args:
            config_name (str): Name of the configure file.
        """
        self.config = load_omega_config(config_name)

        self._camera_vertical_view = self.config["camera_vertical_view"]
        self._dx_threshold_wcs = self.config["dx_threshold_wcs"]
        self._dy_threshold_wcs = self.config["dy_threshold_wcs"]
        self._du_threshold_pcs = self.config["du_threshold_pcs"]
        self._dv_threshold_pcs = self.config["dv_threshold_pcs"]
        self._last_encoder_value = None

        # This list records the of the objects currently on the conveyor
        self._instances_on_conveyor = []

    def select_new_instances(self, grasp_info_list, absolute_encoder_value):
        """Given the segmentation results as a list of GraspInfo, select and return the newly detected instances'
        grasp info with the filtered list.

        Args:
            grasp_info_list (list[GraspInfo]): Input list of GraspInfo objects yield by the segmentation server.
            absolute_encoder_value (float): The absolute encoder value recorded when capturing the image
                                            generating the response. TODO in the dead zone defined by objects found
                                            in the last round, no new object is allowed to emerge.

        Returns:
            list[GraspInfo]: Grasp info for new instances
        """
        self._update_x_translation(absolute_encoder_value)

        # Prune instances too far away from the world frame
        for instance in self._instances_on_conveyor:
            if instance[1] >= self._camera_vertical_view:
                self._instances_on_conveyor.remove(instance)

        filtered_grasp_info_list = []
        grasp_info_list = self._filter_in_single_pic(grasp_info_list)
        for grasp_info in grasp_info_list:
            if self._is_coincide(grasp_info):
                continue

            self._instances_on_conveyor.append(
                [grasp_info.label, grasp_info.grasp_pose_x, grasp_info.grasp_pose_y]
            )
            filtered_grasp_info_list.append(grasp_info)
        return filtered_grasp_info_list

    def _filter_in_single_item(self, item_list):
        """

        Args:
            item_list:

        Returns:
            removed_grasp_info_list(list[GraspInfo]):
        """
        removed_grasp_info_list = []
        for i, item in enumerate(item_list):
            if len(item) == 1:
                removed_grasp_info_list.append(item[0])
                continue
            else:
                for label in item:
                    if label == item[0]:
                        continue
                    if (
                        np.fabs(label.grasp_pose_x - item[0].grasp_pose_x)
                        < self._du_threshold_pcs
                        and np.fabs(label.grasp_pose_y - item[0].grasp_pose_y)
                        < self._dv_threshold_pcs
                    ):
                        if label.label == item[0].label:
                            item[0] = label
                        elif label.label == "capacitance" and item[0].label == "rubber":
                            item[0] = label
                        elif label.label == "PET" and item[0].label == "sponge":
                            item[0] = label
                        elif label.label == "PET" and item[0].label == "pcb":
                            item[0] = label
                        elif label.label == "capacitance" and item[0].label == "can":
                            item[0] = label
                        elif label.label == "capacitance" and item[0].label == "sponge":
                            item[0] = label
                        elif (
                            label.label == "pop can" and item[0].label == "capacitance"
                        ):
                            item[0] = label
                        elif label.label == "pop can" and item[0].label == "can":
                            item[0] = label
                        else:
                            item[0] = label
                    else:
                        continue
                removed_grasp_info_list.append(item[0])
        return removed_grasp_info_list

    def _filter_in_single_pic(self, grasp_info_list):
        """Remove the redundant labels in the single item.

        Args:
            grasp_info_list (list[GraspInfo]):

        Returns:
            grasp_info_list (list[GraspInfo]):

        """
        # if len(grasp_info_list) == 1:
        #     return grasp_info_list
        item_num = 0
        item_list = [[]]
        for i, grasp_info in enumerate(grasp_info_list):
            if grasp_info == grasp_info_list[0]:
                item_list[item_num].append(grasp_info)
                continue
            if (
                np.fabs(grasp_info.grasp_pose_x - grasp_info_list[i - 1].grasp_pose_x)
                < self._du_threshold_pcs
                and np.fabs(
                    grasp_info.grasp_pose_y - grasp_info_list[i - 1].grasp_pose_y
                )
                < self._dv_threshold_pcs
            ):
                # delete redundant label
                item_list[item_num].append(grasp_info)
            else:
                item_num += 1
                item_list.append([])
                item_list[item_num].append(grasp_info)

        removed_grasp_info_list = self._filter_in_single_item(item_list)
        return removed_grasp_info_list

    def _update_x_translation(self, current_encoder_value):
        """Update the recorded x values of the objects on the conveyor with the current encoder value.
        The translation distance between the last update and the current update is returned.

        Args:
            current_encoder_value (float): Absolute encoder value for the current update.

        Returns:
            float: Translation distance between the last update and the current update in mm.
        """
        if self._last_encoder_value is None:
            x_trans = 0.0
        else:
            x_trans = current_encoder_value - self._last_encoder_value
        self._last_encoder_value = current_encoder_value
        for instance in self._instances_on_conveyor:
            instance[1] += x_trans
        return x_trans

    def _is_coincide(self, grasp_info):
        """Check whether the given object to be grasped with grasp_info
        is coincide with an existing object in _instances_on_conveyor.

        Args:
            grasp_info (GraspInfo): Grasp info for the object in consideration.

        Returns:
            bool: True if the object is coincide with a known object, False otherwise.
        """
        if not self._instances_on_conveyor:
            return False

        for instance in self._instances_on_conveyor:
            if (
                instance[0] == grasp_info.label
                and np.fabs(instance[1] - grasp_info.grasp_pose_x)
                < self._dx_threshold_wcs
                and np.fabs(instance[2] - grasp_info.grasp_pose_y)
                < self._dy_threshold_wcs
            ):
                return True
        return False


class RobotHandle(object):
    def __init__(self, robot_class_name, robot_config_name, assigned_object_types):
        """Initialise a handle for using the robot to process objects whose types are listed in assigned_object_types.

        Args:
            robot_class_name (str): Class name of the robot object. This class should be predefined in devices.
            robot_config_name (str): Name of the robot config file.
            assigned_object_types (list[str]): The types of the objects which should be handled by the robot.
        """
        module_path = osp.join(osp.dirname(__file__), "devices.py")
        devices_spec = importlib.util.spec_from_file_location("devices", module_path)
        device_module = devices_spec.loader.load_module("devices")
        RobotObject = getattr(device_module, robot_class_name)
        self._robot_name = robot_config_name
        self._robot = RobotObject(robot_config_name)
        print_info(
            f"Successfully initialized {robot_class_name} with id {self._robot.device_id}"
        )
        self._assigned_object_types = assigned_object_types

    @property
    def robot_name(self):
        """Return the name of the robot."""
        return self._robot_name

    def update_encoder_values(self):
        """Update the instant encoder value and the absolute encoder value."""
        self._robot.update_encoder_values()

    @property
    def absolute_encoder_value(self):
        """Return the absolute encoder value."""
        return self._robot.absolute_encoder_value

    def try_to_grasp(self, grasp_info):
        """Let the robot try to grasp with the given grasp_info.

        Args:
            grasp_info (GraspInfo): Grasping information.

        Returns:
            bool: True if the grasp can be done by the robot, False otherwise.
        """
        if grasp_info.label not in self._assigned_object_types:
            return False
        self._robot.process(grasp_info)
        return True


class TaskManager(object):
    def __init__(self, task_manager_config_name="task_manager"):
        """Initializer of the TaskManager.

        Args:
            task_manager_config_name (str): Name of the YAML configuration file for the TaskManager.
        """
        self.config = load_omega_config(task_manager_config_name)

        # Initialize the segmentation server
        self._segmentation_server = SegmentationServer()
        self._system_test = self._segmentation_server.system_test
        self.all_classes = self._segmentation_server.classes

        # Counters for grasping each class of objects
        self._grasp_counts = {}
        for cls in self.all_classes:
            self._grasp_counts[cls] = 0

        self._grasp_counts_publisher = rospy.Publisher(
            "/grasp_counts", String, queue_size=1
        )

        self.usb_devices = UsbDevices()

        # Initialize the item filter
        self._item_filter = ItemFilter("item_filter")

        # This list stores all the RobotHandle type handles for the robots used in this task.
        self._robot_handles = []

        # A dict whose keys are robot config names and values are assigned object types to the robots.
        self.robot_configs = self.config["robots"]

        for i, robot_config_name in enumerate(self.robot_configs):
            robot_class = load_omega_config(robot_config_name)["class"]
            assigned_object_types = omega_to_list(self.robot_configs[robot_config_name])
            robot_handle = RobotHandle(
                robot_class, robot_config_name, assigned_object_types
            )
            self._robot_handles.append(robot_handle)

        self._conveyor = Conveyor()
        self._camera = Camera.init_camera()

        self._round_flag = 0
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
