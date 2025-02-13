#!/usr/bin/env python3
import rospy
import tf2_ros
import geometry_msgs.msg
import tf.transformations
import math
import matplotlib.pyplot as plt
from sensor_msgs.msg import LaserScan

# Global variables for the robot's pose
x_robot = 0.0
y_robot = 0.0
theta_robot = 0.0

# Global variables for mapping points
map_x = []
map_y = []

# Global variable for the latest laser scan message
latest_scan = None

# Global TF buffer (initialized after node start)
tf_buffer = None

def get_robot_pose():
    """
    Obtain the current robot pose using the transform from 'odom' to 'base_link'.
    """
    global x_robot, y_robot, theta_robot, tf_buffer
    try:
        transform_stamped = tf_buffer.lookup_transform('odom', 'base_footprint',
                                                        rospy.Time(0),
                                                        rospy.Duration(1.0))
        x_robot = transform_stamped.transform.translation.x
        y_robot = transform_stamped.transform.translation.y
        q = transform_stamped.transform.rotation
        _, _, theta_robot = tf.transformations.euler_from_quaternion([q.x, q.y, q.z, q.w])
        rospy.loginfo("Robot pose: x=%.2f, y=%.2f, theta=%.2f", x_robot, y_robot, theta_robot)
    except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
        rospy.logwarn("TF lookup failed in get_robot_pose: %s", e)

def laser_scan_callback(msg):
    """
    Callback to process incoming laser scan messages.
    """
    global latest_scan
    latest_scan = msg

def turn_to_face_object():
    """
    Rotate the robot to face the object head-on by aligning with the angle of the minimum distance measurement.
    """
    global latest_scan
    twist_pub = rospy.Publisher('/cmd_vel', geometry_msgs.msg.Twist, queue_size=10)
    twist = geometry_msgs.msg.Twist()
    rate = rospy.Rate(10)

    while not rospy.is_shutdown() and latest_scan is None:
        rospy.sleep(0.1)

    while not rospy.is_shutdown():
        if latest_scan:
            ranges = latest_scan.ranges
            angles = [latest_scan.angle_min + i * latest_scan.angle_increment for i in range(len(ranges))]
            valid_ranges = [(r, angles[i]) for i, r in enumerate(ranges) if latest_scan.range_min < r < latest_scan.range_max]

            if valid_ranges:
                min_distance, min_angle = min(valid_ranges, key=lambda x: x[0])
                rospy.loginfo(f"Minimum distance: {min_distance}, angle: {min_angle}")

                if abs(min_angle) > 0.05:
                    twist.angular.z = 0.5 if min_angle > 0 else -0.5
                    twist.linear.x = 0.0
                else:
                    twist.angular.z = 0.0
                    twist.linear.x = 0.0
                    twist_pub.publish(twist)
                    rospy.loginfo("Object is now directly in front.")
                    break
                twist_pub.publish(twist)
            rate.sleep()

def move_to_object(distance_threshold):
    """
    Approach the object until a laser scan reading falls below the distance_threshold,
    then execute a circling maneuver.
    """
    global latest_scan
    twist_pub = rospy.Publisher('/cmd_vel', geometry_msgs.msg.Twist, queue_size=10)
    twist = geometry_msgs.msg.Twist()
    rate = rospy.Rate(10)

    rospy.loginfo("Approaching object until distance < %.2f", distance_threshold)
    while not rospy.is_shutdown():
        if latest_scan is not None:
            valid_ranges = [r for r in latest_scan.ranges if latest_scan.range_min < r < latest_scan.range_max]
            if valid_ranges:
                min_distance = min(valid_ranges)
                rospy.loginfo("Min distance: %.2f", min_distance)
                if min_distance > distance_threshold:
                    twist.linear.x = 0.2
                else:
                    twist.linear.x = 0.0
                    twist_pub.publish(twist)
                    rospy.loginfo("Object reached with distance: %.2f", min_distance)
                    trace_object()
                    break
                twist_pub.publish(twist)
        rate.sleep()

def trace_object():
    """
    Circle the object by maintaining a distance with the obstacle at 90 degrees to the left.
    """
    global latest_scan, x_robot, y_robot, map_x, map_y
    twist_pub = rospy.Publisher('/cmd_vel', geometry_msgs.msg.Twist, queue_size=10)
    twist = geometry_msgs.msg.Twist()
    rate = rospy.Rate(10)

    rospy.loginfo("Tracing the object...")
    start_time = rospy.Time.now().to_sec()
    trace_duration = 80

    while not rospy.is_shutdown():
        current_time = rospy.Time.now().to_sec()
        if current_time - start_time > trace_duration:
            rospy.loginfo("Completed tracing for 80 seconds. Stopping.")
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            twist_pub.publish(twist)
            break

        get_robot_pose()
        map_x.append(x_robot)
        map_y.append(y_robot)

        if latest_scan:
            front_distance = latest_scan.ranges[0]
            left_distance = latest_scan.ranges[269]

            # Adjust angular velocity to maintain obstacle on the left at 90 degrees
            target_distance = 0.6  # Slightly increase distance for safer tracking
            distance_error = left_distance - target_distance

            # Proportional controller to maintain a smooth circular path
            angular_speed = max(min(-distance_error * 0.3, 0.15), -0.15)

            # Maintain constant forward speed while adjusting angular velocity
            twist.angular.z = angular_speed
            twist.linear.x = 0.1

            # Ensure the robot slows down significantly when an object appears close in front
            if front_distance < 0.6:
                rospy.loginfo("Obstacle detected in front, turning left to avoid collision.")
                twist.angular.z = 0.5
                twist.linear.x = 0.0

            twist_pub.publish(twist)
        

    rospy.loginfo("Mapping complete, total points collected: %d", len(map_x))
    rospy.loginfo(f"Map X coordinates: {map_x}")
    rospy.loginfo(f"Map Y coordinates: {map_y}")

    plt.figure()
    plt.scatter(map_x, map_y, s=1)
    plt.xlabel('X (meters)')
    plt.ylabel('Y (meters)')
    plt.title('Map of Robot Path During Tracing')
    plt.grid(True)
    plt.axis('equal')
    plt.show(block=True)

if __name__ == '__main__':
    rospy.init_node('mapper')

    tf_buffer = tf2_ros.Buffer()
    tf_listener = tf2_ros.TransformListener(tf_buffer)

    rospy.Subscriber('/scan', LaserScan, laser_scan_callback)

    rospy.sleep(2.0)

    while latest_scan is None and not rospy.is_shutdown():
        rospy.sleep(0.1)

    turn_to_face_object()

    move_to_object(0.5)
