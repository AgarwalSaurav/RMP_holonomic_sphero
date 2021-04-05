# Create a node that publishes location of the robot
# Visualize the robot in rviz to see how the location is changing
# In this example a cubic trajectory is used to travel between two points
# This is for a 3 DoF planar robot
import rospy
from math import sin, cos, sqrt, atan2
from sensor_msgs.msg import JointState

def talker():

    # publish_joint_states is the topic to which the data needs to be published
    # This is the topic the robot will subscribe to and change its position
    pub = rospy.Publisher('/publish_joint_states', JointState, queue_size=10)
    # Name of the node
    rospy.init_node('trajectory_publisher', anonymous=True)
    # Frequency at which the data will be published
    rate = rospy.Rate(30) # 30hz

    # Message type
    new_state = JointState()
    new_state.name = ["x", "y", "theta"]

    # sample start and goal locations
    start_position = [0, 0]
    goal_position = [3, 3]

    # Calculations for cubic trajectory
    del_x = goal_position[0] - start_position[0]
    del_y = goal_position[1] - start_position[1]
    dist_sqr = del_x * del_x + del_y * del_y

    dist = sqrt(dist_sqr)
    max_vel = 0.5
    max_vel_sqr = max_vel * max_vel
    traj_a = -(16 * max_vel * max_vel_sqr)/(27 * dist_sqr)
    traj_b = (4 * max_vel_sqr)/(3 * dist)
    traj_c = 0
    traj_d = 0
    traj_tf = (3 * dist) / (2 * max_vel)

    # Log data
    rospy.loginfo("Total distance: %f", dist)
    rospy.loginfo("Trajectory time: %f", traj_tf)

    cos_angle = del_x / dist
    sin_angle = del_y / dist

    # Get current time
    start_time = rospy.get_rostime()
    while not rospy.is_shutdown():
        time_elapsed = (rospy.get_rostime() - start_time)
        time_secs = time_elapsed.secs + time_elapsed.nsecs/1e9
        time_secs_sqr = time_secs * time_secs
        if(time_secs < traj_tf):
            pt = traj_a * time_secs * time_secs_sqr + traj_b * time_secs_sqr + traj_c * time_secs + traj_d
            new_state.header.stamp = rospy.get_rostime()
            # Write position of the robot to the message data
            new_state.position = [pt * cos_angle, pt * sin_angle, time_secs * atan2(del_x, del_y)/traj_tf]
            # Send the message
            pub.publish(new_state);
        rate.sleep()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
