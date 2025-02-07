#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
import math

def scan_callback(msg):
    valid_ranges = [r for r in msg.ranges if not math.isinf(r) and not math.isnan(r)]
    
    if not valid_ranges:
        rospy.loginfo("No valid laser scan readings.")
        return
    
    min_range = min(valid_ranges)
    max_range = max(valid_ranges)
    
    min_index = msg.ranges.index(min_range)
    max_index = msg.ranges.index(max_range)
    
    angle_increment = msg.angle_increment
    min_angle = msg.angle_min + (min_index * angle_increment)
    max_angle = msg.angle_min + (max_index * angle_increment)

    rospy.loginfo(f"\nTotal Valid Readings: {len(valid_ranges)}"
                  f"\nClosest Point: {min_range:.2f} meters at {math.degrees(min_angle):.2f} degrees"
                  f"\nFarthest Point: {max_range:.2f} meters at {math.degrees(max_angle):.2f} degrees\n")

def laser_listener():
    rospy.init_node('laser_scan_listener', anonymous=True)
    rospy.Subscriber('/scan', LaserScan, scan_callback)
    rospy.spin()

if __name__ == '__main__':
    laser_listener()