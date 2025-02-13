#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import math

def move_in_circle():
    rospy.init_node('circle_mover', anonymous=True)
    velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)
    radius = 5.0
    angular_velocity = 0.2
    linear_velocity = radius * angular_velocity
    while not rospy.is_shutdown():
        twist = Twist()
        twist.linear.x = linear_velocity
        twist.angular.z = angular_velocity
        velocity_publisher.publish(twist)
        rate.sleep()

if __name__ == '__main__':
    move_in_circle()
