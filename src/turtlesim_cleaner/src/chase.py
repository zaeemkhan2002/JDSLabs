#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt


class TurtleChaser:
    def __init__(self):
        # Initialize ROS node
        rospy.init_node('turtle_chaser', anonymous=True)

        # Publisher to move turtle2
        self.velocity_publisher = rospy.Publisher('/turtle2/cmd_vel', Twist, queue_size=10)

        # Subscriber to get turtle1's pose
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose', Pose, self.update_pose)

        # Store the target turtle's pose (turtle1)
        self.target_pose = Pose()
        self.rate = rospy.Rate(10)  # 10 Hz

    def update_pose(self, data):
        """Callback function to update turtle1's position."""
        self.target_pose = data

    def euclidean_distance(self, current_pose, goal_pose):
        """Calculate Euclidean distance between two turtles."""
        return sqrt(pow((goal_pose.x - current_pose.x), 2) +
                    pow((goal_pose.y - current_pose.y), 2))

    def chase_turtle(self):
        """Make turtle2 chase turtle1."""
        # Subscriber to get turtle2's pose
        turtle2_pose = Pose()
        rospy.Subscriber('/turtle2/pose', Pose, lambda data: setattr(turtle2_pose, 'x', data.x) or setattr(turtle2_pose, 'y', data.y) or setattr(turtle2_pose, 'theta', data.theta))

        vel_msg = Twist()

        while not rospy.is_shutdown():
            # Calculate distance between turtle2 and turtle1
            distance = self.euclidean_distance(turtle2_pose, self.target_pose)

            # If turtle2 is far, move toward turtle1
            if distance > 0.5:
                vel_msg.linear.x = 1.5 * distance  # Proportional control for speed
                vel_msg.angular.z = 4.0 * (atan2(self.target_pose.y - turtle2_pose.y, 
                                                 self.target_pose.x - turtle2_pose.x) - turtle2_pose.theta)

                # Publish velocity command to turtle2
                self.velocity_publisher.publish(vel_msg)
            else:
                # Stop turtle2 when close
                vel_msg.linear.x = 0
                vel_msg.angular.z = 0
                self.velocity_publisher.publish(vel_msg)

            self.rate.sleep()


if __name__ == '__main__':
    try:
        chaser = TurtleChaser()
        chaser.chase_turtle()
    except rospy.ROSInterruptException:
        pass
