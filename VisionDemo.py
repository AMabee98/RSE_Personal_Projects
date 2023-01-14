from sre_constants import BRANCH
from niryo_robot_python_ros_wrapper.ros_wrapper import *
import sys
import rospy

rospy.init_node('niryo_blockly_interpreted_code')
n = NiryoRosWrapper()

try:
    n.move_pose(0.16, 0, 0.35, 0, 1.57, 0) #Move to observation pose
    if n.detect_object('default_workspace', ObjectShape.CIRCLE, ObjectColor.RED)[0]:
        n.vision_pick_w_obs_pose('default_workspace', -5/1000.0, ObjectShape.SQUARE, ObjectColor.RED, [0.16, 0, 0.35, 0, 1.57, 0])[0]
        n.move_pose(0.125, 0.197, 0.041, 0, 1.57, 0) #Stack peice if found.
    
    n.move_pose(0.16, 0, 0.35, 0, 1.57, 0) #Move to observation pose
    if n.detect_object('default_workspace', ObjectShape.SQUARE, ObjectColor.RED)[0]:
        n.vision_pick_w_obs_pose('default_workspace', -5/1000.0, ObjectShape.SQUARE, ObjectColor.RED, [0.16, 0, 0.35, 0, 1.57, 0])[0]
        n.move_pose(0.125, 0.197, 0.041, 0, 1.57, 0) #Stack peice if found.

    
    n.move_pose(0.16, 0, 0.35, 0, 1.57, 0) #Move to observation pose
    if n.detect_object('default_workspace', ObjectShape.CIRCLE, ObjectColor.GREEN)[0]:
        n.vision_pick_w_obs_pose('default_workspace', -5/1000.0, ObjectShape.SQUARE, ObjectColor.GREEN, [0.16, 0, 0.35, 0, 1.57, 0])[0]
        n.move_pose(0.125, 0.197, 0.041, 0, 1.57, 0) #Stack peice if found.
    
    n.move_pose(0.16, 0, 0.35, 0, 1.57, 0) #Move to observation pose
    if n.detect_object('default_workspace', ObjectShape.SQUARE, ObjectColor.GREEN)[0]:
        n.vision_pick_w_obs_pose('default_workspace', -5/1000.0, ObjectShape.SQUARE, ObjectColor.GREEN, [0.16, 0, 0.35, 0, 1.57, 0])[0]
        n.move_pose(0.125, 0.197, 0.041, 0, 1.57, 0) #Stack peice if found.


    n.move_pose(0.16, 0, 0.35, 0, 1.57, 0) #Move to observation pose
    if n.detect_object('default_workspace', ObjectShape.CIRCLE, ObjectColor.BLUE)[0]:
        n.vision_pick_w_obs_pose('default_workspace', -5/1000.0, ObjectShape.SQUARE, ObjectColor.RED, [0.16, 0, 0.35, 0, 1.57, 0])[0]
        n.move_pose(0.125, 0.197, 0.041, 0, 1.57, 0) #Stack peice if found.
    
    n.move_pose(0.16, 0, 0.35, 0, 1.57, 0) #Move to observation pose
    if n.detect_object('default_workspace', ObjectShape.SQUARE, ObjectColor.BLUE)[0]:
        n.vision_pick_w_obs_pose('default_workspace', -5/1000.0, ObjectShape.SQUARE, ObjectColor.BLUE, [0.16, 0, 0.35, 0, 1.57, 0])[0]
        n.move_pose(0.125, 0.197, 0.041, 0, 1.57, 0) #Stack peice if found.

    n.move_to_sleep_pose()
    n.set_learning_mode(True)

except NiryoRosWrapperException as e:
   sys.stderr.write(str(e))