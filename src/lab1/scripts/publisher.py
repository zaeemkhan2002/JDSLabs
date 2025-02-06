#!/usr/bin/env python3
import rospy
from lab1.msg import ComplexNumber


def talker():
    pub = rospy.Publisher('complex_number', ComplexNumber, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        msg = ComplexNumber()
        msg.real = rospy.get_param('~real', 1.0)
        msg.imaginary = rospy.get_param('~imaginary', 2.0)
        rospy.loginfo(f"Publishing: real = {msg.real}, imaginary = {msg.imaginary}")
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
