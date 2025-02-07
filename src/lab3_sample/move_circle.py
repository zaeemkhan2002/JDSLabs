#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist

def move_in_circle():
    rospy.init_node('turtlebot3_circle', anonymous=True)

    velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()

    radius = 5.0  
    linear_speed = 0.2  
    angular_speed = linear_speed / radius

    vel_msg.linear.x = linear_speed
    vel_msg.angular.z = angular_speed

    rospy.loginfo("Moving TurtleBot3 in a circle with a 5m radius!")

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        velocity_publisher.publish(vel_msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        move_in_circle()
    except rospy.ROSInterruptException:
        pass