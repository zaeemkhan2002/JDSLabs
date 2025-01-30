#!/usr/bin/env python3
import rospy
from lab1.msg import ComplexNumber


def talker():
    pub = rospy.Publisher('complex_number', ComplexNumber, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        msg = ComplexNumber()
        msg.real = 1
        for idx in range(1, 20):
            msg.real = idx
            msg.imaginary = idx + 0.5
            rospy.loginfo(f"Sending: {msg.real} + {msg.imaginary}i")
            pub.publish(msg)
            rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
