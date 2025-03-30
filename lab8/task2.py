#!/usr/bin/env python3
import rospy
import math
import tf
import time
from geometry_msgs.msg import PoseStamped, Quaternion
from nav_msgs.msg import Odometry
from robomaster import robot

class PIDController:
    def __init__(self, kp, ki, kd, dt, output_limit=None):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt
        self.output_limit = output_limit
        self.integral_error = 0.0
        self.previous_error = 0.0

    def reset(self):
        self.integral_error = 0.0
        self.previous_error = 0.0

    def compute_output(self, current_error):
        p_term = self.kp * current_error
        self.integral_error += current_error * self.dt
        i_term = self.ki * self.integral_error
        d_term = self.kd * (current_error - self.previous_error) / self.dt
        self.previous_error = current_error
        output = p_term + i_term + d_term
        if self.output_limit is not None:
            min_out, max_out = self.output_limit
            output = max(min_out, min(output, max_out))
        return output

def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def angle_difference(current, target):
    return (target - current + math.pi) % (2 * math.pi) - math.pi

class RoboMasterGoalFollower:
    def __init__(self):
        rospy.init_node("robomaster_goal_follower_with_odom", anonymous=True)

        self.ep_robot = robot.Robot()
        self.ep_robot.initialize(conn_type="rndis")
        self.ep_chassis = self.ep_robot.chassis

        self.odom_pub = rospy.Publisher("/odom", Odometry, queue_size=10)
        self.tf_broadcaster = tf.TransformBroadcaster()

        self.odom_sub = rospy.Subscriber("/odom", Odometry, self.odom_callback)
        self.goal_sub = rospy.Subscriber( "/move_base/NavfnROS/plan", PoseStamped, self.goal_callback)

        self.robot_x = 0.0
        self.robot_y = 0.0
        self.robot_theta = 0.0

        self.goal_x = None
        self.goal_y = None
        self.goal_received = False

        self.dt = 0.1
        self.dist_pid = PIDController(1.2, 0.0, 0.2, self.dt, output_limit=(-0.5, 0.5))
        self.ang_pid = PIDController(2.0, 0.0, 0.1, self.dt, output_limit=(-1.5, 1.5))

        self.dist_tolerance = 0.1
        self.ang_tolerance = 0.05

    def goal_callback(self, msg):
        self.goal_x = msg.pose.position.x
        self.goal_y = msg.pose.position.y
        self.goal_received = True
        self.dist_pid.reset()
        self.ang_pid.reset()
        rospy.loginfo(f"New goal: ({self.goal_x:.2f}, {self.goal_y:.2f})")

    def publish_odometry(self, linear, angular):
        current_time = rospy.Time.now()
        quat = tf.transformations.quaternion_from_euler(0, 0, self.robot_theta)

        self.tf_broadcaster.sendTransform(
            (self.robot_x, self.robot_y, 0),
            quat,
            current_time,
            "base_link",
            "odom"
        )

        odom = Odometry()
        odom.header.stamp = current_time
        odom.header.frame_id = "odom"
        odom.child_frame_id = "base_link"
        odom.pose.pose.position.x = self.robot_x
        odom.pose.pose.position.y = self.robot_y
        odom.pose.pose.orientation = Quaternion(*quat)
        odom.twist.twist.linear.x = linear
        odom.twist.twist.angular.z = angular
        self.odom_pub.publish(odom)

    def go_to_goal(self):
        rate = rospy.Rate(1.0 / self.dt)

        while not rospy.is_shutdown():
            if not self.goal_received:
                rate.sleep()
                continue

            dx = self.goal_x - self.robot_x
            dy = self.goal_y - self.robot_y
            dist_error = euclidean_distance(self.robot_x, self.robot_y, self.goal_x, self.goal_y)
            desired_theta = math.atan2(dy, dx)
            ang_error = angle_difference(self.robot_theta, desired_theta)

            if dist_error < self.dist_tolerance and abs(ang_error) < self.ang_tolerance:
                rospy.loginfo("Goal reached.")
                self.ep_chassis.drive_speed(x=0, y=0, z=0, timeout=0.1)
                self.goal_received = False
                continue

            linear_cmd = self.dist_pid.compute_output(dist_error)
            angular_cmd = self.ang_pid.compute_output(ang_error)

            angular_deg = math.degrees(angular_cmd)
            self.ep_chassis.drive_speed(x=linear_cmd, y=0, z=angular_deg, timeout=0.1)

            self.robot_x += linear_cmd * math.cos(self.robot_theta) * self.dt
            self.robot_y += linear_cmd * math.sin(self.robot_theta) * self.dt
            self.robot_theta += angular_cmd * self.dt
            self.robot_theta = (self.robot_theta + math.pi) % (2 * math.pi) - math.pi

            self.publish_odometry(linear_cmd, angular_cmd)

            rospy.loginfo(f"Pose=({self.robot_x:.2f}, {self.robot_y:.2f}, θ={math.degrees(self.robot_theta):.1f}°) | "
                          f"Linear={linear_cmd:.2f}, Angular={angular_deg:.2f}")

            rate.sleep()

    def odom_callback(self, msg):
        pass

if __name__ == "__main__":
    try:
        controller = RoboMasterGoalFollower()
        controller.go_to_goal()
    except rospy.ROSInterruptException:
        pass