#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import time

PI = 3.1415926535897

def move_in_square():
    # Initialize the ROS node
    rospy.init_node('square_motion', anonymous=True)
    
    # Create a publisher for the velocity topic
    velocity_publisher = rospy.Publisher('/turtle2/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()

    # User input for speed & side length
    linear_speed = float(input("Enter linear speed (m/s): "))  # Speed along x-axis
    angular_speed = float(input("Enter angular speed (rad/s): "))  # Speed of rotation
    side_length = float(input("Enter the side length (m): "))  # Distance to move forward

    rate = rospy.Rate(10)  # 10 Hz

    for _ in range(4):  # Loop 4 times to create a square
        # Move forward
        vel_msg.linear.x = linear_speed
        vel_msg.angular.z = 0
        rospy.loginfo(f"Moving forward {side_length} meters")
        
        t0 = rospy.Time.now().to_sec()
        current_distance = 0
        while current_distance < side_length:
            velocity_publisher.publish(vel_msg)
            t1 = rospy.Time.now().to_sec()
            current_distance = linear_speed * (t1 - t0)
        
        # Stop before turning
        vel_msg.linear.x = 0
        velocity_publisher.publish(vel_msg)
        time.sleep(1)  # Wait before turning

        # Rotate 90 degrees (clockwise)
        vel_msg.angular.z = -angular_speed  # Negative for clockwise rotation
        rospy.loginfo("Turning 90 degrees")
        
        t0 = rospy.Time.now().to_sec()
        current_angle = 0
        while current_angle < (PI / 2):
            velocity_publisher.publish(vel_msg)
            t1 = rospy.Time.now().to_sec()
            current_angle = angular_speed * (t1 - t0)
        
        # Stop before next move
        vel_msg.angular.z = 0
        velocity_publisher.publish(vel_msg)
        time.sleep(1)  # Wait before moving again

    rospy.loginfo("Square motion completed!")

    # Stop the robot completely
    vel_msg.linear.x = 0
    vel_msg.angular.z = 0
    velocity_publisher.publish(vel_msg)

if __name__ == '__main__':
    try:
        move_in_square()
    except rospy.ROSInterruptException:
        pass
