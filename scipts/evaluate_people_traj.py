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
X_ROW = 1
Y_ROW = 2
X_MAX = 17.0
X_MIN = -4
TIME_ROW = 0
OFFSET  = 5

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


if __name__ == "__main__":
    dir_name = argvs[1]

    dwaStop = Policy("k",".")
    dwaMin = Policy("b",".")
    dwaMax = Policy("r",".")
    dwaRobust = Policy("g",".")
    for tmp_dir in sorted(os.listdir(dir_name)):
        target = dir_name + "/" + tmp_dir+ "/"
        max_length = 0.0
        for file in sorted(os.listdir(target)):
            file_path = target+"/"+file
            if file_path.split("/")[-1].split("-")[0] != "robot" and file_path.split("/")[-1].split("_")[0] != "robot":
                data = readCsv(file_path)
            else:
                continue

            # if not tmp_dir == "test44_1238_B_2018-08-30-17-15-43":
                # continue
            #先頭行を除いて、pose, time取得
            people_position = data[:,X_ROW:Y_ROW+1].astype(np.float)
            time_list = data[:,TIME_ROW].astype(np.float)

            # print tmp_dir, ":", people_position.shape
            print tmp_dir, ":", file

            #スタート時の位置、時間を求める
            pre_pose = [float(people_position[0,0]),float(people_position[0,1])]

            #経過時間を求める
            start_time = time_list[0]
            end_time = time_list[-1]

            tmp_length = 0.0
            count = -1
            for current_people in people_position:
                count = count + 1
                if count < OFFSET:
                    continue
                if count > people_position.shape[0]-OFFSET:
                    break

                tmp_length = tmp_length + math.sqrt((pre_pose[0] - current_people[0])*(pre_pose[0] - current_people[0]) + (pre_pose[1] - current_people[1])*(pre_pose[1] - current_people[1]))
                pre_pose = current_people

                # ax.plot(current_robot[0], current_robot[1], color)
                # ax.hold(True)
            if max_length < tmp_length:
                max_length = tmp_length

        if tmp_dir.split("_")[-1] == "A":
            dwaStop.array = np.append(dwaStop.array, np.array([max_length]))
            dwaStop.length = dwaStop.length + max_length
            dwaStop.count = dwaStop.count + 1
            dwaStop.time = dwaStop.time + end_time - start_time
            color = dwaStop.color
            marker = dwaStop.marker
        if tmp_dir.split("_")[-1] == "B":
            dwaMin.array = np.append(dwaMin.array, np.array([max_length]))
            dwaMin.length = dwaMin.length + max_length
            dwaMin.count = dwaMin.count + 1
            dwaMin.time = dwaMin.time + end_time - start_time
            color = dwaMin.color
            marker = dwaMin.marker
        if tmp_dir.split("_")[-1] == "C":
            dwaMax.array = np.append(dwaMax.array, np.array([max_length]))
            dwaMax.length = dwaMax.length + max_length
            dwaMax.count = dwaMax.count + 1
            dwaMax.time = dwaMax.time + end_time - start_time
            color = dwaMax.color
            marker = dwaMax.marker
        if tmp_dir.split("_")[-1] == "D":
            dwaRobust.array = np.append(dwaRobust.array, np.array([max_length]))
            dwaRobust.length = dwaRobust.length + max_length
            dwaRobust.count = dwaRobust.count + 1
            dwaRobust.time = dwaRobust.time + end_time - start_time
            color = dwaRobust.color
            marker = dwaRobust.marker

            # debug
        ax.plot(people_position[:,0], people_position[:,1], color = color, marker = marker)
        ax.hold(True)
    # print "Stop: length ave: %.2f" %(np.average(dwaStop.array)), "stdev: %.2f" %(np.sqrt(np.var(dwaStop.array))), " time: %.2f" %(dwaStop.time/dwaStop.count), dwaStop.count
    # print "Min: length ave: %.2f" %(np.average(dwaMin.array)), "stdev: %.2f" %(np.sqrt(np.var(dwaMin.array))), " time: %.2f" %(dwaMin.time/dwaMin.count), dwaMin.count
    # print "Max: length ave: %.2f" %(np.average(dwaMax.array)), "stdev: %.2f" %(np.sqrt(np.var(dwaMax.array))), " time: %.2f" %(dwaMax.time/dwaMax.count), dwaMax.count
    # print "Robust: length ave: %.2f" %(np.average(dwaRobust.array)), "stdev: %.2f" %(np.sqrt(np.var(dwaRobust.array))), " time: %.2f" %(dwaRobust.time/dwaRobust.count), dwaRobust.count
    print dwaMin.array
    print
    print dwaRobust.array
    ax.set_aspect('equal', adjustable='box')
    plt.show()
