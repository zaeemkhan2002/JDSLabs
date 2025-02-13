#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
import math

def laser_scan_callback(msg):
    valid_readings = 0
    closest_range = float('inf')
    closest_angle = 0.0
    farthest_range = 0.0
    farthest_angle = 0.0

    for i, r in enumerate(msg.ranges):
        if msg.range_min <= r <= msg.range_max:
            valid_readings += 1

            if r < closest_range:
                closest_range = r
                closest_angle = msg.angle_min + i * msg.angle_increment

            if r > farthest_range:
                farthest_range = r
                farthest_angle = msg.angle_min + i * msg.angle_increment

    print(f"Total valid readings: {valid_readings}")

    if valid_readings > 0:
      print(f"Range of closest point: {closest_range:.2f} m, Angle: {math.degrees(closest_angle):.2f} deg")
      print(f"Range of farthest point: {farthest_range:.2f} m, Angle: {math.degrees(farthest_angle):.2f} deg")
    else:
      print("No valid laser scan readings received.")



if __name__ == '__main__':
    rospy.init_node('turtlebot3_laserscan', anonymous=True)
    rospy.Subscriber('/scan', LaserScan, laser_scan_callback)
    rospy.spin()
