#!/usr/bin/env python3
import math
import rospy
from lab1.msg import ComplexNumber

def callback(data):
    magnitude = (data.real**2 + data.imaginary**2) ** 0.5
    phase_radians = math.atan2(data.imaginary, data.real)
    phase_degrees = phase_radians * (180 / math.pi)
    rospy.loginfo(f'\nReceived: real={data.real}, imaginary={data.imaginary}i\nMagnitude: {magnitude}, Phase: {phase_radians}\n{rospy.get_caller_id()}\n')

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('complex_number', ComplexNumber, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
