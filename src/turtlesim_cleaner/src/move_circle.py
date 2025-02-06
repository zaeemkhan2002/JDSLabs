#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
PI = 3.1415926535897

def move_in_circle():
    # Initialize the ROS node
    rospy.init_node('circle_motion', anonymous=True)
    
    # Create a publisher for the velocity topic
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()

    # User input for speed
    linear_speed = float(input("Enter linear speed (m/s): "))  # Speed along x-axis
    angular_speed = float(input("Enter angular speed (rad/s): "))  # Speed of rotation

    vel_msg.linear.x = linear_speed  # Move forward
    vel_msg.angular.z = angular_speed  # Rotate

    rate = rospy.Rate(10)  # 10 Hz
    while not rospy.is_shutdown():
        velocity_publisher.publish(vel_msg)
        rate.sleep()

    vel_msg.linear.x = 0
    vel_msg.angular.z = 0
    velocity_publisher.publish(vel_msg)

if __name__ == '__main__':
    try:
        move_in_circle()
    except rospy.ROSInterruptException:
        pass
