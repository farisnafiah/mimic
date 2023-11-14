#!/usr/bin/python3

import rospy
import tf
from tf.transformations import euler_from_quaternion, quaternion_from_euler


if __name__ == '__main__':
    rospy.init_node('tf_a')
    listener = tf.TransformListener()

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
            (trans,rot) = listener.lookupTransform('/test_table_origin', '/test_gantryorigin', rospy.Time(0))
            (roll, pitch, yaw) = euler_from_quaternion (rot)
            print(trans, rot)
            print(trans, [roll, pitch, yaw])
        except (tf.LookupException, tf.ConnectivityException):
            continue

    rate.sleep()