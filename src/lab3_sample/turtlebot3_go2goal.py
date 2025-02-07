#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
import math

x = 0.0
y = 0.0
yaw = 0.0

def odom_callback(msg):
    global x, y, yaw
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y

    orientation_q = msg.pose.pose.orientation
    _, _, yaw = euler_from_quaternion([orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w])

def move_to_goal(goal_x, goal_y):
    rospy.init_node('turtlebot3_go2goal', anonymous=True)
    
    vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('/odom', Odometry, odom_callback)

    vel_msg = Twist()
    rate = rospy.Rate(10)  
    
    while not rospy.is_shutdown():
        distance = math.sqrt((goal_x - x)**2 + (goal_y - y)**2)
        angle_to_goal = math.atan2(goal_y - y, goal_x - x)
        angle_error = (angle_to_goal - yaw + math.pi) % (2 * math.pi) - math.pi  

        vel_msg.linear.x = min(0.5 * distance, 0.2)
        vel_msg.angular.z = 1.5 * angle_error
        
        vel_pub.publish(vel_msg)

        if distance < 0.1: 
            break
        
        # rate.sleep()

    vel_msg.linear.x = 0
    vel_msg.angular.z = 0
    vel_pub.publish(vel_msg)
    rospy.loginfo("Goal reached!")

if __name__ == '__main__':
    try:
        goal_x = float(input("Enter goal x-coordinate: "))
        goal_y = float(input("Enter goal y-coordinate: "))
        
        move_to_goal(goal_x, goal_y)
    
    except rospy.ROSInterruptException:
        pass