#!/usr/bin/env python3

import rospy
import tf2_ros
import geometry_msgs.msg
import tf.transformations

if __name__ == '__main__':
    rospy.init_node('dynamic_transform_publisher')
    br = tf2_ros.TransformBroadcaster()
    rate = rospy.Rate(10.0)  

    while not rospy.is_shutdown():
        transform_stamped = geometry_msgs.msg.TransformStamped()
        transform_stamped.header.stamp = rospy.Time.now()
        transform_stamped.header.frame_id = "world"  
        transform_stamped.child_frame_id = "base_link" 
        
        robot_x = 1.0  
        robot_y = 2.0  
        robot_theta = 0.5  

        transform_stamped.transform.translation.x = robot_x
        transform_stamped.transform.translation.y = robot_y
        transform_stamped.transform.translation.z = 0.0
        q = tf.transformations.quaternion_from_euler(0, 0, robot_theta) 
        transform_stamped.transform.rotation.x = q[0]
        transform_stamped.transform.rotation.y = q[1]
        transform_stamped.transform.rotation.z = q[2]
        transform_stamped.transform.rotation.w = q[3]

        br.sendTransform(transform_stamped)

        rate.sleep()
