#!/usr/bin/env python3

from sensor_msgs.msg import LaserScan
import rospy
import tf2_ros
import geometry_msgs.msg
import tf.transformations
import math
import matplotlib.pyplot as plt
import numpy as np


x_robot = 0.0
y_robot = 0.0
theta_robot = 0.0
map_x = []
map_y = []

def get_robot_pose():
    global x_robot, y_robot, theta_robot
    tf_buffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tf_buffer)
    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
            transform_stamped = tf_buffer.lookup_transform('world', 'base_link', rospy.Time(0))
            x_robot = transform_stamped.transform.translation.x
            y_robot = transform_stamped.transform.translation.y
            q = transform_stamped.transform.rotation
            _, _, theta_robot = tf.transformations.euler_from_quaternion([q.x, q.y, q.z, q.w])
            print(f"Theta robot: {theta_robot}")
            return

def laser_scan_callback(msg):
    global map_x, map_y
    ranges = msg.ranges
    angles = [msg.angle_min + i * msg.angle_increment for i in range(len(ranges))]

    for i, r in enumerate(ranges):
        if msg.range_min < r < msg.range_max:
            angle_robot = angles[i]
            x_robot_local = r * math.cos(angle_robot)
            y_robot_local = r * math.sin(angle_robot)

            x_world = x_robot + x_robot_local * math.cos(theta_robot) - y_robot_local * math.sin(theta_robot)
            y_world = y_robot + x_robot_local * math.sin(theta_robot) + y_robot_local * math.cos(theta_robot)
            
            map_x.append(x_world)
            map_y.append(y_world)

def move_to_object(distance_threshold):
    twist_pub = rospy.Publisher('/cmd_vel', geometry_msgs.msg.Twist, queue_size=10)
    twist = geometry_msgs.msg.Twist()
    
    while not rospy.is_shutdown():
        if min(laser_scan.ranges) > distance_threshold:
            twist.linear.x = 0.2
        else:
            twist.linear.x = 0.0
            break
        print(f"{min(laser_scan.ranges)} -> {distance_threshold}")
        twist_pub.publish(twist)
        rospy.sleep(0.1)

    while not rospy.is_shutdown():
        twist.angular.z = 0.2  
        twist.linear.x = 0.1 
        twist_pub.publish(twist)
        rospy.sleep(0.1)

if __name__ == '__main__':
    rospy.init_node('mapper')
    laser_scan_sub = rospy.Subscriber('/scan', LaserScan, laser_scan_callback)
    
    print("Hello")
    get_robot_pose()

    laser_scan = rospy.wait_for_message('/scan', LaserScan)
    move_to_object(0.5) 

    plt.scatter(map_x, map_y, s=1)
    plt.xlabel('X (meters)')
    plt.ylabel('Y (meters)')
    plt.title('Map of Object')
    plt.grid(True)
    plt.axis('equal')
    plt.show()
