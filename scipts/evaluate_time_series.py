#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import shutil
import time
import math

fig = plt.figure(figsize=(20,20),dpi=200)
ax1 = fig.add_subplot(2,2,1) #左上
ax2 = fig.add_subplot(2,2,2) #右上
ax3 = fig.add_subplot(2,2,3) #左下
ax4 = fig.add_subplot(2,2,4) #右下


argvs = sys.argv
FILE_NAME = "robot.csv"
PEDESTRIAN = ["PEDESTRIAN_0_0.csv", "PEDESTRIAN_1_1.csv", "PEDESTRIAN_2_2.csv", "PEDESTRIAN_3_3.csv", "PEDESTRIAN_4_4.csv", "PEDESTRIAN_5_5.csv", "PEDESTRIAN_6_6.csv", "PEDESTRIAN_7_7.csv", "PEDESTRIAN_8_8.csv", "PEDESTRIAN_9_9.csv"]
X_ROW = 1
Y_ROW = 2
TIME_ROW = 0
X_MAX = 100.0 #ゴール
X_MIN = -100.0 #スタート
#X_MAX = 16.0 #ゴール
#X_MIN = -9.0 #スタート

if len(argvs) != 2:
    print "usage python %s <target dir>" % argvs[0]
    exit()


def readCsv(filename):
    data = np.loadtxt(filename, delimiter=',', dtype = str)
    return data

if __name__ == "__main__":
    target_dir = argvs[1]
    policy_list = ["A5", "E5", "F5", "I5"]
    #policy_list = ["E5"]
    time_waypoints = np.arange(0,30,5)

    collision_A =0
    collision_E =0
    collision_F =0
    collision_I =0

    for policy_dir in sorted(os.listdir(target_dir)):
        tmp_dir = policy_dir.split("_")
        if not (tmp_dir[-1] == policy_list[0]):#基準
            continue
        ax1.cla()
        ax2.cla()
        ax3.cla()
        ax4.cla()
        for policy_name in policy_list:
            actor_data = []
            tmp_policy_dir = "_".join(tmp_dir[:-1]) + "_" + policy_name
            if policy_name == "A5":
                target_ax = ax1
            elif policy_name == "E5":
                target_ax = ax2
            elif policy_name == "F5":
                target_ax = ax3
            elif policy_name == "I5":
                target_ax = ax4

            for file in os.listdir(os.path.join(target_dir, tmp_policy_dir)):
                #csvファイルを読み込む
                file_path = os.path.join(target_dir, tmp_policy_dir, file)
                data = readCsv(file_path)

                #ロボットの軌跡ファイル以外に対して
                if not "robot" in file:
                    actor_data.append(data)
                else:
                    robot_data = data
            #robot_data = readCsv(os.path.join(target_dir, tmp_policy_dir, FILE_NAME))

            robot_position = robot_data[0:,X_ROW:Y_ROW+1].astype(np.float)
            time_list = robot_data[0:, TIME_ROW].astype(np.float)
            print tmp_policy_dir, ":", robot_position.shape[0]

            #X軸の値からスタート時の位置、時間を求める
            min_index = np.argmin(np.abs(robot_position[:,0]-X_MIN))
            #min_index = 0
            max_index = np.argmin(np.abs(robot_position[:,0]-X_MAX))

            #対象時間を表示する
            for time_waypoint in time_waypoints:
                target_index = np.argmin(np.abs(time_list-time_list[0]-time_waypoint))
                if target_index > min_index and target_index < max_index:
                    #ロボットの位置に時間を表示
                    target_ax.text(robot_position[target_index,0], robot_position[target_index,1], str(time_waypoint), color="blue")

                    #人の位置に時間を表示
                for i in range(len(actor_data)):
                    tmp_actor = np.array(actor_data[i])
                    actor_pose_stamped = tmp_actor[0:,0:3].astype(np.float)
                    actor_target_index = np.argmin(np.abs(actor_pose_stamped[:,0]-time_list[0]-time_waypoint))
                    if actor_target_index != len(actor_pose_stamped) -1:
                        target_ax.text(actor_pose_stamped[actor_target_index,1], actor_pose_stamped[actor_target_index,2], str(time_waypoint), color="red")


            #ロボットの位置を表示
            target_ax.plot(robot_position[min_index:max_index+1,0], robot_position[min_index:max_index+1,1], color = "b", marker = ".")

            #人の位置を表示
            for i in range(len(actor_data)):
                tmp_actor = np.array(actor_data[i])
                actor_pose_stamped = tmp_actor[0:,0:3].astype(np.float)
                #if "Long" in policy_dir:#ロボット進行方向の人流に対して
                if False:
                    actor_min_index = np.argmin(np.abs(actor_pose_stamped[:,1]-X_MIN))
                    actor_max_index = np.argmin(np.abs(actor_pose_stamped[:,1]-X_MAX))
                    target_ax.plot(actor_pose_stamped[actor_min_index:actor_max_index,1], actor_pose_stamped[actor_min_index:actor_max_index,2], color = "r")
                else:
                    target_ax.plot(actor_pose_stamped[:-1,1], actor_pose_stamped[:-1,2], color = "r")

            #人とロボットが近い時は色を変えて表示
            collision =0
            lethal = 0
            tmp_length = 0
            pre_pose = np.array([robot_position[min_index,0], robot_position[min_index,1]])
            for count in range(min_index, max_index+1):
                current_time = time_list[count]
                current_robot = robot_position[count,:]

                tmp_length +=  np.linalg.norm(current_robot-pre_pose)
                pre_pose = current_robot
                for i in range(len(actor_data)):
                    tmp_actor = np.array(actor_data[i])
                    actor_pose_stamped = tmp_actor[0:,0:3].astype(np.float)
                    actor_target_index = np.argmin(np.abs(actor_pose_stamped[:,0]-current_time))
                    current_tmp_actor = actor_pose_stamped[actor_target_index, 1:3]
                    if np.linalg.norm(current_robot-current_tmp_actor) < 1.0:
                        target_ax.plot(current_robot[0], current_robot[1], color = "y", marker = ".")
                        target_ax.plot(current_tmp_actor[0], current_tmp_actor[1], color = "y", marker = ".")
                        collision += 1
                    if np.linalg.norm(current_robot-current_tmp_actor) < 0.5:
                        target_ax.plot(current_robot[0], current_robot[1], color = "c", marker = ".")
                        target_ax.plot(current_tmp_actor[0], current_tmp_actor[1], color = "c", marker = ".")
                        lethal +=1

            print collision
            target_ax.text(0.1, 0.9, "collision: %s" % collision, transform=target_ax.transAxes)
            target_ax.text(0.1, 0.8, "lethal: %s" % lethal, transform=target_ax.transAxes)
            target_ax.text(0.1, 0.7, "path length: %.2f" % tmp_length, transform=target_ax.transAxes)
            target_ax.text(0.1, 0.6, "time: %.2f" % (time_list[max_index] - time_list[min_index]), transform=target_ax.transAxes)

            #target_ax.hold(True)
            target_ax.set_aspect('equal', adjustable='box')

            if policy_name == "A5":
                collision_A += collision
            elif policy_name == "E5":
                collision_E += collision
            elif policy_name == "F5":
                collision_F += collision
            elif policy_name == "I5":
                collision_I += collision
        #plt.tight_layout()
        plt.savefig(tmp_policy_dir.split("/")[-1]+".png")
        #plt.show()
        print collision_A, collision_E, collision_F, collision_I
