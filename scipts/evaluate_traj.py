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
ax = fig.add_subplot(1,1,1)

argvs = sys.argv
FILE_NAME = "_slash_multi_modal_pose.csv"
X_ROW = 9
Y_ROW = 10
X_MAX = 17.0
X_MIN = 2.0
SECS_ROW = 4
NSECS_ROW = 5

if len(argvs) != 2:
    print "usage python %s <target dir>" % argvs[0]
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
        self.time_array = np.array([])


if __name__ == "__main__":
    target_dir = argvs[1]

    dwaStop = Policy("k",".")
    dwaMin = Policy("b",".")
    dwaMax = Policy("r",".")
    dwaRobust = Policy("g",".")
    for dir in sorted(os.listdir(target_dir)):
        data = readCsv(target_dir + "/" + dir+ "/" + FILE_NAME)

        # if not dir == "test44_1238_B_2018-08-30-17-15-43":
            # continue
        #先頭行を除いて、pose, time取得
        robot_position = data[1:,X_ROW:Y_ROW+1].astype(np.float)
        secs_list = data[1:, SECS_ROW]
        nsecs_list = data[1:, NSECS_ROW]

        print dir, ":", robot_position.shape[0]

        #スタート時の位置、時間を求める
        min_index = np.argmin(np.abs(robot_position[:,0]-X_MIN))
        pre_pose = [float(robot_position[min_index,0]),float(robot_position[min_index,1])]

        #経過時間を求める
        start_time = float(secs_list[min_index] + "." + nsecs_list[min_index].zfill(9))
        max_index = np.argmin(np.abs(robot_position[:,0]-X_MAX))
        end_time = float(secs_list[max_index] + "." + nsecs_list[max_index].zfill(9))

        tmp_length = 0.0
        count = -1
        for current_robot in robot_position:
            count = count + 1
            if current_robot[0] < X_MIN:
                continue

            if current_robot[0] > X_MAX:
                break

            tmp_length = tmp_length + math.sqrt((pre_pose[0] - current_robot[0])*(pre_pose[0] - current_robot[0]) + (pre_pose[1] - current_robot[1])*(pre_pose[1] - current_robot[1]))
            pre_pose = current_robot

            # ax.plot(current_robot[0], current_robot[1], color)
            # ax.hold(True)

        if dir.split("_")[2] == "A" or dir.split("_")[1] == "A":
            dwaStop.array = np.append(dwaStop.array, np.array([tmp_length]))
            dwaStop.length = dwaStop.length + tmp_length
            dwaStop.count = dwaStop.count + 1
            dwaStop.time = dwaStop.time + end_time - start_time
            dwaStop.time_array = np.append(dwaStop.time_array, np.array([end_time - start_time]))
            color = dwaStop.color
            marker = dwaStop.marker
        if dir.split("_")[2] == "B" or dir.split("_")[1] == "B":
            dwaMin.array = np.append(dwaMin.array, np.array([tmp_length]))
            dwaMin.length = dwaMin.length + tmp_length
            dwaMin.count = dwaMin.count + 1
            dwaMin.time = dwaMin.time + end_time - start_time
            dwaMin.time_array = np.append(dwaMin.time_array, np.array([end_time - start_time]))
            color = dwaMin.color
            marker = dwaMin.marker
        if dir.split("_")[2] == "C" or dir.split("_")[1] == "C":
            dwaMax.array = np.append(dwaMax.array, np.array([tmp_length]))
            dwaMax.length = dwaMax.length + tmp_length
            dwaMax.count = dwaMax.count + 1
            dwaMax.time = dwaMax.time + end_time - start_time
            dwaMax.time_array = np.append(dwaMax.time_array, np.array([end_time - start_time]))
            color = dwaMax.color
            marker = dwaMax.marker
        if dir.split("_")[2] == "D" or dir.split("_")[1] == "D":
            dwaRobust.array = np.append(dwaRobust.array, np.array([tmp_length]))
            dwaRobust.length = dwaRobust.length + tmp_length
            dwaRobust.count = dwaRobust.count + 1
            dwaRobust.time = dwaRobust.time + end_time - start_time
            dwaRobust.time_array = np.append(dwaRobust.time_array, np.array([end_time - start_time]))
            color = dwaRobust.color
            marker = dwaRobust.marker

        # debug
        ax.plot(robot_position[min_index:max_index+1,0], robot_position[min_index:max_index+1,1], color = color, marker = marker)
        ax.hold(True)
    # print "Stop: length ave: %.2f" %(np.average(dwaStop.array)), "stdev: %.2f" %(np.sqrt(np.var(dwaStop.array))), " time: %.2f" %(dwaStop.time/dwaStop.count), dwaStop.count
    # print "Min: length ave: %.2f" %(np.average(dwaMin.array)), "stdev: %.2f" %(np.sqrt(np.var(dwaMin.array))), " time: %.2f" %(dwaMin.time/dwaMin.count), dwaMin.count
    # print "Max: length ave: %.2f" %(np.average(dwaMax.array)), "stdev: %.2f" %(np.sqrt(np.var(dwaMax.array))), " time: %.2f" %(dwaMax.time/dwaMax.count), dwaMax.count
    # print "Robust: length ave: %.2f" %(np.average(dwaRobust.array)), "stdev: %.2f" %(np.sqrt(np.var(dwaRobust.array))), " time: %.2f" %(dwaRobust.time/dwaRobust.count), dwaRobust.count
    print "Stop: length ave: %.2f" %(np.average(dwaStop.array)), "stdev: %.2f" %(np.sqrt(np.var(dwaStop.array))), " time: %.2f" %(np.average(dwaStop.time_array)), np.std(dwaStop.time_array)
    print "Min: length ave: %.2f" %(np.average(dwaMin.array)), "stdev: %.2f" %(np.sqrt(np.var(dwaMin.array))), " time: %.2f" %(np.average(dwaMin.time_array)), np.std(dwaMin.time_array)
    print "Max: length ave: %.2f" %(np.average(dwaMax.array)), "stdev: %.2f" %(np.sqrt(np.var(dwaMax.array))), " time: %.2f" %(np.average(dwaMax.time_array)), np.std(dwaMax.time_array)
    print "Robust: length ave: %.2f" %(np.average(dwaRobust.array)), "stdev: %.2f" %(np.sqrt(np.var(dwaRobust.array))), " time: %.2f" %(np.average(dwaRobust.time_array)), np.std(dwaRobust.time_array)
    ax.set_aspect('equal', adjustable='box')
    plt.show()
