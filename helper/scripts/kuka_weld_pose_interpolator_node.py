#!/usr/bin/env python3
import rospy
import csv
from std_msgs.msg import Float64MultiArray
import os
from math import sqrt
import subprocess
import sys

weld_start_pose = None
weld_stop_pose = None

def weld_start_pose_callback(msg):
    global weld_start_pose
    weld_start_pose = msg.data
    rospy.loginfo("weld_start_pose %s", weld_start_pose)

def weld_stop_pose_callback(msg):
    global weld_stop_pose
    weld_stop_pose = msg.data  
    rospy.loginfo("weld_stop_pose %s", weld_stop_pose)

    output_folder = rospy.get_param("~output_folder", "/home/interpolated_poses/")
    output_file = rospy.get_param("~output_file", "interpolated_weld_poses.csv")

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
        
    interpolate_and_save_poses(output_folder, output_file)

def euclidean_distance_calc(pose1, pose2):
    x2 = (pose1[0] - pose2[0]) ** 2
    y2 = (pose1[1] - pose2[1]) ** 2
    z2 = (pose1[2] - pose2[2]) ** 2
    r2 = x2 + y2 + z2
    return sqrt(r2)

def interpolate_and_save_poses(output_folder, output_file):
    if weld_start_pose is None or weld_stop_pose is None:
        rospy.logerr("Start or end pose is missing.")
        return

    euclidean_distance = euclidean_distance_calc(weld_start_pose, weld_stop_pose)
    rospy.loginfo("euclidean_distance in mm: %s", euclidean_distance)

    intervel = rospy.get_param("~intervel", 0.1) # in seconds
    velocity = rospy.get_param("~velocity", 0.01) # meter/seconds

    duration = (euclidean_distance/1000) / velocity
    num_interpolations = duration / intervel
    rospy.loginfo("num_interpolations: %s", int(num_interpolations))

    interpolated_poses = []
    for i in range(int(num_interpolations) + 1):
        alpha = float(i) / num_interpolations
        interpolated_pose = interpolate_poses(weld_start_pose, weld_stop_pose, alpha)
        interpolated_poses.append(interpolated_pose)

    iona_topic_name = rospy.get_param("~iona_topic_name", "iona_topic_name")
    iona_path_name = rospy.get_param("~iona_path_name", "iona_path_name")

    with open(output_folder + output_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for i, pose in enumerate(interpolated_poses):
            writer.writerow([iona_topic_name] + [iona_path_name] + pose)

    # for testing purpose
    output_file_2 = "trimmed_interpolated_weld_poses.csv"
    trimmed_interpolated_pose_list = trim_list(interpolated_poses)

    with open(output_folder + output_file_2, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for i, pose in enumerate(trimmed_interpolated_pose_list):
            writer.writerow([iona_topic_name] + [iona_path_name] + pose)

    try:
        if os.stat(output_folder + output_file).st_size > 0:
            rospy.loginfo("%s interpolated poses wrote to csv file ", len(interpolated_poses))
        if os.stat(output_folder + output_file_2).st_size > 0:
            rospy.loginfo("%s trimmed interpolated poses wrote to csv file ", len(trimmed_interpolated_pose_list))

            rospy.loginfo("exiting node to run path converter dotnet program")
            rospy.signal_shutdown('Exit command received')
        else:
            rospy.logerr("csv file empty")
    except OSError:
        print ("No file")

    # bash_command = output_folder + "./convert_file.sh" 
    # subprocess.Popen(bash_command, shell=True)

def trim_list(lst):
    # Calculate the number of elements to remove from each end
    pose_list_trim_percentage = 1
    num_to_remove = int(len(lst) * (pose_list_trim_percentage/100))
    
    # Ensure we're not removing more elements than the list contains
    num_to_remove = min(num_to_remove, len(lst)//2)
    
    # Trim the list
    trimmed_lst = lst[num_to_remove:-num_to_remove]
    
    return trimmed_lst

def interpolate_poses(pose1, pose2, alpha):
    position1 = [pose1[0], pose1[1], pose1[2]]
    position2 = [pose2[0], pose2[1], pose2[2]]
    orientation1 = [pose2[3], pose2[4], pose2[5]]
    orientation2 = [pose2[3], pose2[4], pose2[5]]

    interpolated_position = [
        position1[0] + alpha * (position2[0] - position1[0]),
        position1[1] + alpha * (position2[1] - position1[1]),
        position1[2] + alpha * (position2[2] - position1[2])
    ]

    interpolated_orientation = [
        orientation1[0] + alpha * (orientation2[0] - orientation1[0]),
        orientation1[1] + alpha * (orientation2[1] - orientation1[1]),
        orientation1[2] + alpha * (orientation2[2] - orientation1[2])
    ]

    return [
        round(interpolated_position[0], 4),
        round(interpolated_position[1], 4),
        round(interpolated_position[2], 4),
        round(interpolated_orientation[0], 4),
        round(interpolated_orientation[1], 4),
        round(interpolated_orientation[2], 4)
    ]

def main():
    global interpolated_pose_pub
    rospy.init_node('kuka_weld_pose_interpolator_node')

    kuka_weld_start_topic_name = rospy.get_param("~arcon_vector_pose_topic_name", "/kuka_arcon_pose_vector")
    kuka_weld_stop_topic_name = rospy.get_param("~arcoff_vector_pose_topic_name", "/kuka_arcoff_pose_vector")

    weld_start_pose_sub = rospy.Subscriber(kuka_weld_start_topic_name, Float64MultiArray, weld_start_pose_callback)
    weld_stop_pose_sub = rospy.Subscriber(kuka_weld_stop_topic_name, Float64MultiArray, weld_stop_pose_callback)
    
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass


