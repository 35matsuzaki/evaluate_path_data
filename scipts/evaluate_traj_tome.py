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
ax = fig.add_subplot(1,2,1)
ax2 = fig.add_subplot(1,2,2)

argvs = sys.argv
FILE_NAME = "_slash_multi_modal_pose.csv"
X_ROW = 1
Y_ROW = 2
TIME_ROW = 0
X_MAX = 6
X_MIN = -6.0
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
        self.result_dict = {}
        self.time_array = np.array([])

class dataManager:
    def setResult(self, dir, length, time):
        path_name = dir.split("_")[0]
        if path_name in self.result_dict:
            tmp_list = self.result_dict[path_name]
            tmp_list.append([time,length])
            tmp_dict = {path_name:tmp_list}
            self.result_dict.update(tmp_dict)
        else:
            tmp_dict = {path_name:[[time,length]]}
            self.result_dict.update(tmp_dict)


    def saveResult(self,dir):
        if dir.split("_")[-1] == "A":
            print "test"


if __name__ == "__main__":
    target_dir = argvs[1]

    dwaStop = Policy("k",".")
    dwaMin = Policy("b",".")
    dwaMax = Policy("r",".")
    dwaRobust = Policy("g",".")
    for dir in sorted(os.listdir(target_dir)):
        print dir
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
        # self.setResult(dir,tmp_length, end_time - start_time)

        if dir.split("_")[-1] == "A":
            dwaStop.array = np.append(dwaStop.array, np.array([tmp_length]))
            dwaStop.length = dwaStop.length + tmp_length
            dwaStop.count = dwaStop.count + 1
            dwaStop.time = dwaStop.time + end_time - start_time
            dwaStop.time_array = np.append(dwaStop.time_array, np.array([end_time - start_time]))
            color = dwaStop.color
            marker = dwaStop.marker
        if dir.split("_")[-1] == "B":
            dwaMin.array = np.append(dwaMin.array, np.array([tmp_length]))
            dwaMin.length = dwaMin.length + tmp_length
            dwaMin.count = dwaMin.count + 1
            dwaMin.time = dwaMin.time + end_time - start_time
            dwaMin.time_array = np.append(dwaMin.time_array, np.array([end_time - start_time]))
            color = dwaMin.color
            marker = dwaMin.marker
        if dir.split("_")[-1] == "C":
            dwaMax.array = np.append(dwaMax.array, np.array([tmp_length]))
            dwaMax.length = dwaMax.length + tmp_length
            dwaMax.count = dwaMax.count + 1
            dwaMax.time = dwaMax.time + end_time - start_time
            dwaMax.time_array = np.append(dwaMax.time_array, np.array([end_time - start_time]))
            color = dwaMax.color
            marker = dwaMax.marker
        if dir.split("_")[-1] == "D":
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

    ax2.hist([dwaStop.array, dwaMin.array, dwaMax.array,dwaRobust.array ],color=['black','blue', 'red', 'green'])
    print "Stop: length ave: %.2f" %(np.average(dwaStop.array)), "stdev: %.2f" %(np.sqrt(np.var(dwaStop.array))), " time: %.2f" %(np.average(dwaStop.time_array)), np.std(dwaStop.time_array)
    print "Min: length ave: %.2f" %(np.average(dwaMin.array)), "stdev: %.2f" %(np.sqrt(np.var(dwaMin.array))), " time: %.2f" %(np.average(dwaMin.time_array)), np.std(dwaMin.time_array)
    print "Max: length ave: %.2f" %(np.average(dwaMax.array)), "stdev: %.2f" %(np.sqrt(np.var(dwaMax.array))), " time: %.2f" %(np.average(dwaMax.time_array)), np.std(dwaMax.time_array)
    print "Robust: length ave: %.2f" %(np.average(dwaRobust.array)), "stdev: %.2f" %(np.sqrt(np.var(dwaRobust.array))), " time: %.2f" %(np.average(dwaRobust.time_array)), np.std(dwaRobust.time_array)
    ax.set_aspect('equal', adjustable='box')
    plt.show()
