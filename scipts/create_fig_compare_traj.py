#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import shutil
import time
import math

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
# ax1 = fig.add_subplot(2,2,1)
# ax2 = fig.add_subplot(2,2,2)
# ax3 = fig.add_subplot(2,2,3)
# ax4 = fig.add_subplot(2,2,4)

argvs = sys.argv
FILE_NAME = "_slash_multi_modal_pose.csv"
X_ROW = 1 #8: vel_x gt
Y_ROW = 2 #9: vel_y_gt
TIME_ROW = 0
X_MAX = 6
X_MIN = -6.0
SECS_ROW = 4
NSECS_ROW = 5

if len(argvs) != 1:
    print "usage python %s" % argvs[0]
    exit()


def readCsv(filename):
    data = np.loadtxt(filename, delimiter=',', dtype = str)
    return data

class Policy:#stop, min, max, robust
    def __init__(self, color, marker):
        self.min = 100.0
        self.max = -1.0
        self.length = 0.0
        self.color = color
        self.count = 0
        self.time = 0.0
        self.marker = marker
        self.array = np.array([])


if __name__ == "__main__":
#    target_dir = argvs[1]
    target_dir = "/home/sango/workspace/evaluate/gazebo_actor/20180725_test37"

    dwaStop = Policy("k",".")
    dwaMin = Policy("b",".")
    dwaMax = Policy("r",".")
    dwaRobust = Policy("g",".")
    for dir in sorted(os.listdir(target_dir)):
        tmp_dir = target_dir + "/" + dir
        for file in sorted(os.listdir(tmp_dir)):
            if "robot" in file:
                FILE_NAME = file

        data = readCsv(target_dir + "/" + dir+ "/" + FILE_NAME)

        # if not dir == "test44_1238_B_2018-08-30-17-15-43":
            # continue
        #先頭行を除いて、pose, time取得
        robot_position = data[1:,X_ROW:Y_ROW+1].astype(np.float)
        secs_list = data[1:, SECS_ROW]
        nsecs_list = data[1:, NSECS_ROW]
        time_list = data[1:, TIME_ROW].astype(np.float)

        print dir, ":", robot_position.shape[0]

        #スタート時の位置、時間を求める
        min_index = np.argmin(np.abs(robot_position[:,0]-X_MIN))
        pre_pose = [float(robot_position[min_index,0]),float(robot_position[min_index,1])]

        #経過時間を求める
        # start_time = float(secs_list[min_index] + "." + nsecs_list[min_index].zfill(9))
        start_time = time_list[min_index]
        max_index = np.argmin(np.abs(robot_position[:,0]-X_MAX))
        end_time = time_list[max_index]
        # end_time = float(secs_list[max_index] + "." + nsecs_list[max_index].zfill(9))

        if dir.split("_")[-1] == "A":
            # ax1.plot(np.arange(0,data[:,X_ROW].shape[0],1),data[:,X_ROW], ".")
            ax1.plot(data[:,X_ROW], data[:,Y_ROW], "k", label="without DWA")
        if dir.split("_")[-1] == "B":
            # ax2.plot(np.arange(0,data[:,X_ROW].shape[0],1),data[:,X_ROW], ".")
            ax1.plot(data[:,X_ROW], data[:,Y_ROW], "r", label="min")
        if dir.split("_")[-1] == "C":
            # ax3.plot(np.arange(0,data[:,X_ROW].shape[0],1),data[:,X_ROW], ".")
            ax1.plot(data[:,X_ROW], data[:,Y_ROW], "b", label="max")
        if dir.split("_")[-1] == "D":
            # ax4.plot(np.arange(0,data[:,X_ROW].shape[0],1),data[:,X_ROW], ".")
            ax1.plot(data[:,X_ROW], data[:,Y_ROW], "g", label="variable")

    ax1.set_aspect('equal', adjustable='box')
    ax1.legend()
    ax1.set_ylim(-1,6)
#    plt.show()
    plt.savefig("compare_traj_on_no_avoid.eps")
