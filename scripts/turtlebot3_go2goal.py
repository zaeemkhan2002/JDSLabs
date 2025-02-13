#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
import math

x = 0.0
y = 0.0
theta = 0.0

def odom_callback(msg):
    global x, y, theta
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y
    rot_q = msg.pose.pose.orientation
    (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])

def go_to_goal(goal_x, goal_y):
    rospy.init_node('go2goal', anonymous=True)
    velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    odom_subscriber = rospy.Subscriber('/odom', Odometry, odom_callback)
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        goal_theta = math.atan2(goal_y - y, goal_x - x)
        angular_error = goal_theta - theta
        if abs(angular_error) > math.pi:
            angular_error = 2 * math.pi - abs(angular_error) if angular_error > 0 else -(2 * math.pi - abs(angular_error))

        linear_error = math.sqrt((goal_x - x)**2 + (goal_y - y)**2)

        twist = Twist()

        if linear_error > 0.1: 
            twist.linear.x = 0.2 if linear_error > 0.5 else 0.1 
            twist.angular.z = 0.3 * angular_error  
        else:
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            break

        velocity_publisher.publish(twist)
        rate.sleep()

    rospy.loginfo("Goal reached!")

if __name__ == '__main__':
    goal_x = float(input("Enter goal x coordinate: "))
    goal_y = float(input("Enter goal y coordinate: "))
    go_to_goal(goal_x, goal_y)
