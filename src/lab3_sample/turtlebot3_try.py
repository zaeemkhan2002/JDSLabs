#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
import math

class TurtleBot3GoToGoal:
    def __init__(self):
        rospy.init_node('turtlebot3_go2goal', anonymous=True)
        
        # Create a publisher to send velocity commands
        self.vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        
        # Subscribe to the odometry topic to get the robot’s position
        rospy.Subscriber('/odom', Odometry, self.odom_callback)
        
        self.x = 0
        self.y = 0
        self.yaw = 0  # Orientation of the robot
        
        self.rate = rospy.Rate(10)  # 10 Hz

    def odom_callback(self, msg):
        """Callback function to update the robot's position."""
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y

        # Extract orientation as Euler angles
        orientation_q = msg.pose.pose.orientation
        _, _, self.yaw = euler_from_quaternion([orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w])

    def move_to_goal(self, goal_x, goal_y):
        """Move TurtleBot3 to the specified goal position."""
        vel_msg = Twist()
        
        while not rospy.is_shutdown():
            # Compute distance and angle to goal
            distance = math.sqrt((goal_x - self.x)**2 + (goal_y - self.y)**2)
            angle_to_goal = math.atan2(goal_y - self.y, goal_x - self.x)
            
            # Compute angle difference
            angle_error = angle_to_goal - self.yaw
            
            # Normalize the angle between -pi and pi
            angle_error = (angle_error + math.pi) % (2 * math.pi) - math.pi
            
            # Proportional Control (P-Control)
            linear_speed = 0.5 * distance  # Adjust the gain as needed
            angular_speed = 1.5 * angle_error  # Adjust the gain as needed
            
            # Set velocity
            vel_msg.linear.x = min(linear_speed, 0.2)  # Limit speed
            vel_msg.angular.z = angular_speed
            
            # Publish velocity
            self.vel_pub.publish(vel_msg)
            
            # Stop if close enough
            if distance < 0.1:
                break

            self.rate.sleep()
        
        # Stop the robot
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        self.vel_pub.publish(vel_msg)
        rospy.loginfo("Goal reached!")

if __name__ == '__main__':
    try:
        bot = TurtleBot3GoToGoal()
        
        # Define goal coordinates (Modify as needed)
        goal_x = float(input("Enter goal x-coordinate: "))
        goal_y = float(input("Enter goal y-coordinate: "))
        
        rospy.sleep(1)  # Allow time for odom updates
        bot.move_to_goal(goal_x, goal_y)
    
    except rospy.ROSInterruptException:
        pass