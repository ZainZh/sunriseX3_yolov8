from src.tools.smartbin import SmartBin
import rospy

if __name__ == "__main__":
    rospy.init_node("task_manager")
    node = SmartBin("task_manager")
    rospy.loginfo("Task manager ready")
    rospy.spin()