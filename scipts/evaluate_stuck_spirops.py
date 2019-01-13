#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import shutil
import time
import math
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import statsmodels.api as sm
from statsmodels.formula.api import ols
import statsmodels.stats.anova as anova
import pandas as pd

fig = plt.figure()
ax = fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,2)
ax3 = fig.add_subplot(2,2,3)
ax4 = fig.add_subplot(2,2,4)


argvs = sys.argv
FILE_NAME = "robot.csv"
X_ROW = 8 # 8:odom, 10:cmd
Y_ROW = 9 # 9:odom, 11:cmd
TIME_ROW = 0
# X_MAX = 8.0 #ゴール tome
# X_MIN = -7 #スタート tome
X_MAX = 10.0 #ゴール spirops
X_MIN = -4.0 #スタート spirops
#X_MAX = 16.0 #ゴール
#X_MIN = -9.0 #スタート

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
    dwaMinOnly = Policy("c",".")
    dwaMaxOnly = Policy("m",".")

    for policy_dir in sorted(os.listdir(target_dir)):
        for file in sorted(os.listdir(os.path.join(target_dir, policy_dir))):#robot ファイルを探す
            # print file
            if "robot" in file:
                FILE_NAME = file
                break


        print "target:", FILE_NAME
        data = readCsv(os.path.join(target_dir, policy_dir, FILE_NAME))

        robot_velocity = data[0:,X_ROW:Y_ROW+1].astype(np.float)
        robot_position = data[0:,1:3].astype(np.float)

        time_list = data[0:, TIME_ROW].astype(np.float)
        print policy_dir, ":", robot_velocity.shape[0]

        #スタート時の位置、時間を求める
        min_index = np.argmin(np.abs(robot_velocity[:,0]-X_MIN))
        #min_index = 0
        pre_pose = np.array([robot_velocity[min_index,0], robot_velocity[min_index,1]])

        #経過時間を求める
        # start_time = float(secs_list[min_index] + "." + nsecs_list[min_index].zfill(9))
        start_time = time_list[min_index]
        max_index = np.argmin(np.abs(robot_velocity[:,0]-X_MAX))
        end_time = time_list[max_index]
        # end_time = float(secs_list[max_index] + "." + nsecs_list[max_index].zfill(9))

        count = -1
        #経路ごとのスタートとゴール位置を統一する
        tmp_stuck_time = 0.0
        stuck_flag = False
        start_stuck_time = time_list[0]
        for index, current_robot in enumerate(robot_velocity):
            count = count + 1
            current_robot_pose = robot_position[index]
            if current_robot_pose[0] < X_MIN:
                continue

            if current_robot_pose[0]  > X_MAX:
                break

            vel_norm = np.linalg.norm(current_robot[0])
            threthold = 0.1
            if not stuck_flag and vel_norm<=threthold:
                stuck_flag = True
                start_stuck_time = time_list[index]
            elif stuck_flag and vel_norm > threthold:
                stuck_flag = False
                tmp_stuck_time += time_list[index] - start_stuck_time

            # ax.plot(current_robot[0], current_robot[1], color)
            # ax.hold(True)
        # self.setResult(dir,tmp_stuck_time, end_time - start_time)

        if policy_dir.split("_")[-1] == "A5":
            dwaStop.array = np.append(dwaStop.array, np.array([tmp_stuck_time]))
            dwaStop.length = dwaStop.length + tmp_stuck_time
            dwaStop.count = dwaStop.count + 1
            dwaStop.time = dwaStop.time + end_time - start_time
            dwaStop.time_array = np.append(dwaStop.time_array, np.array([end_time - start_time]))
            color = dwaStop.color
            marker = dwaStop.marker
        elif policy_dir.split("_")[-1] == "B5":
            dwaMin.array = np.append(dwaMin.array, np.array([tmp_stuck_time]))
            dwaMin.length = dwaMin.length + tmp_stuck_time
            dwaMin.count = dwaMin.count + 1
            dwaMin.time = dwaMin.time + end_time - start_time
            dwaMin.time_array = np.append(dwaMin.time_array, np.array([end_time - start_time]))
            color = dwaMin.color
            marker = dwaMin.marker
        elif policy_dir.split("_")[-1] == "C5":
            dwaMax.array = np.append(dwaMax.array, np.array([tmp_stuck_time]))
            dwaMax.length = dwaMax.length + tmp_stuck_time
            dwaMax.count = dwaMax.count + 1
            dwaMax.time = dwaMax.time + end_time - start_time
            dwaMax.time_array = np.append(dwaMax.time_array, np.array([end_time - start_time]))
            color = dwaMax.color
            marker = dwaMax.marker
        elif policy_dir.split("_")[-1] == "I5":
            dwaRobust.array = np.append(dwaRobust.array, np.array([tmp_stuck_time]))
            dwaRobust.length = dwaRobust.length + tmp_stuck_time
            dwaRobust.count = dwaRobust.count + 1
            dwaRobust.time = dwaRobust.time + end_time - start_time
            dwaRobust.time_array = np.append(dwaRobust.time_array, np.array([end_time - start_time]))
            color = dwaRobust.color
            marker = dwaRobust.marker
        elif policy_dir.split("_")[-1] == "E5":
            dwaMinOnly.array = np.append(dwaMinOnly.array, np.array([tmp_stuck_time]))
            dwaMinOnly.length = dwaMinOnly.length + tmp_stuck_time
            dwaMinOnly.count = dwaMinOnly.count + 1
            dwaMinOnly.time = dwaMinOnly.time + end_time - start_time
            dwaMinOnly.time_array = np.append(dwaMinOnly.time_array, np.array([end_time - start_time]))
            color = dwaMinOnly.color
            marker = dwaMinOnly.marker
        elif policy_dir.split("_")[-1] == "F5":
            dwaMaxOnly.array = np.append(dwaMaxOnly.array, np.array([tmp_stuck_time]))
            dwaMaxOnly.length = dwaMaxOnly.length + tmp_stuck_time
            dwaMaxOnly.count = dwaMaxOnly.count + 1
            dwaMaxOnly.time = dwaMaxOnly.time + end_time - start_time
            dwaMaxOnly.time_array = np.append(dwaMaxOnly.time_array, np.array([end_time - start_time]))
            color = dwaMaxOnly.color
            marker = dwaMaxOnly.marker

        else:
            continue
        # debug
        ax.plot(robot_velocity[min_index:max_index+1,0], robot_velocity[min_index:max_index+1,1], color = color, marker = marker)
        ax.hold(True)

    print "path length shapiro test"
    print "A:", stats.shapiro(dwaStop.array)
    print "B:", stats.shapiro(dwaMin.array)
    print "C:", stats.shapiro(dwaMax.array)
    print "D:", stats.shapiro(dwaRobust.array)
    print "E:", stats.shapiro(dwaMinOnly.array)
    print "F:", stats.shapiro(dwaMaxOnly.array)

    print
    print "time shapiro test"
    print "A:", stats.shapiro(dwaStop.time_array)
    print "B:", stats.shapiro(dwaMin.time_array)
    print "C:", stats.shapiro(dwaMax.time_array)
    print "D:", stats.shapiro(dwaRobust.time_array)
    print "E:", stats.shapiro(dwaMinOnly.time_array)
    print "F:", stats.shapiro(dwaMaxOnly.time_array)


    print "path length t test"
    print "A vs B:", stats.ttest_rel(dwaStop.array, dwaMin.array)
    print "A vs C:", stats.ttest_rel(dwaStop.array, dwaMax.array)
    print "A vs D:", stats.ttest_rel(dwaStop.array, dwaRobust.array)
    print "A vs E:", stats.ttest_rel(dwaStop.array, dwaMinOnly.array)
    print "A vs F:", stats.ttest_rel(dwaStop.array, dwaMaxOnly.array)
    print "B vs C:", stats.ttest_rel(dwaMin.array, dwaMax.array)
    print "B vs D:", stats.ttest_rel(dwaMin.array, dwaRobust.array)
    print "B vs E:", stats.ttest_rel(dwaMin.array, dwaMinOnly.array)
    print "B vs F:", stats.ttest_rel(dwaMin.array, dwaMaxOnly.array)
    print "C vs D:", stats.ttest_rel(dwaMax.array, dwaRobust.array)
    print "C vs E:", stats.ttest_rel(dwaMax.array, dwaMinOnly.array)
    print "C vs F:", stats.ttest_rel(dwaMax.array, dwaMaxOnly.array)
    print "D vs E:", stats.ttest_rel(dwaRobust.array, dwaMinOnly.array)
    print "D vs F:", stats.ttest_rel(dwaRobust.array, dwaMaxOnly.array)
    print "E vs F:", stats.ttest_rel(dwaMinOnly.array, dwaMaxOnly.array)

    print
    print "time t test"
    print "A vs B:", stats.ttest_rel(dwaStop.time_array, dwaMin.time_array)
    print "A vs C:", stats.ttest_rel(dwaStop.time_array, dwaMax.time_array)
    print "A vs D:", stats.ttest_rel(dwaStop.time_array, dwaRobust.time_array)
    print "A vs E:", stats.ttest_rel(dwaStop.time_array, dwaMinOnly.time_array)
    print "A vs F:", stats.ttest_rel(dwaStop.time_array, dwaMaxOnly.time_array)
    print "B vs C:", stats.ttest_rel(dwaMin.time_array, dwaMax.time_array)
    print "B vs D:", stats.ttest_rel(dwaMin.time_array, dwaRobust.time_array)
    print "B vs E:", stats.ttest_rel(dwaMin.time_array, dwaMinOnly.time_array)
    print "B vs F:", stats.ttest_rel(dwaMin.time_array, dwaMaxOnly.time_array)
    print "C vs D:", stats.ttest_rel(dwaMax.time_array, dwaRobust.time_array)
    print "C vs E:", stats.ttest_rel(dwaMax.time_array, dwaMinOnly.time_array)
    print "C vs F:", stats.ttest_rel(dwaMax.time_array, dwaMaxOnly.time_array)
    print "D vs E:", stats.ttest_rel(dwaRobust.time_array, dwaMinOnly.time_array)
    print "D vs F:", stats.ttest_rel(dwaRobust.time_array, dwaMaxOnly.time_array)
    print "E vs F:", stats.ttest_rel(dwaMinOnly.time_array, dwaMaxOnly.time_array)




    ax2.hist([dwaStop.array, dwaMin.array, dwaMax.array,dwaRobust.array ],color=['black','blue', 'red', 'green'])
    print "Stop: length ave: %.2f" %(np.average(dwaStop.array)), "stdev: %.2f" %(np.sqrt(np.var(dwaStop.array))), " time: %.2f" %(np.average(dwaStop.time_array)), np.std(dwaStop.time_array)
    print "Min: length ave: %.2f" %(np.average(dwaMin.array)), "stdev: %.2f" %(np.sqrt(np.var(dwaMin.array))), " time: %.2f" %(np.average(dwaMin.time_array)), np.std(dwaMin.time_array)
    print "Max: length ave: %.2f" %(np.average(dwaMax.array)), "stdev: %.2f" %(np.sqrt(np.var(dwaMax.array))), " time: %.2f" %(np.average(dwaMax.time_array)), np.std(dwaMax.time_array)
    print "Robust: length ave: %.2f" %(np.average(dwaRobust.array)), "stdev: %.2f" %(np.sqrt(np.var(dwaRobust.array))), " time: %.2f" %(np.average(dwaRobust.time_array)), np.std(dwaRobust.time_array)
    print "MinOnly: length ave: %.2f" %(np.average(dwaMinOnly.array)), "stdev: %.2f" %(np.sqrt(np.var(dwaMinOnly.array))), " time: %.2f" %(np.average(dwaMinOnly.time_array)), np.std(dwaMinOnly.time_array)
    print "MaxOnly: length ave: %.2f" %(np.average(dwaMaxOnly.array)), "stdev: %.2f" %(np.sqrt(np.var(dwaMaxOnly.array))), " time: %.2f" %(np.average(dwaMaxOnly.time_array)), np.std(dwaMaxOnly.time_array)
    ax.set_aspect('equal', adjustable='box')

    ax3.scatter(np.arange(0,dwaStop.array.shape[0]), dwaStop.array-dwaRobust.array, c="black", s = 100)
    ax3.scatter(np.arange(0,dwaMin.array.shape[0]), dwaMin.array-dwaRobust.array, c="red", s = 100)
    ax3.scatter(np.arange(0,dwaMax.array.shape[0]), dwaMax.array-dwaRobust.array, c="blue", s = 100)
    ax3.plot([0,14], [0,0],"blue", linestyle='dashed')

    ax4.scatter(np.arange(0,dwaStop.time_array.shape[0]), dwaStop.time_array-dwaRobust.time_array, c="black", s = 100)
    ax4.scatter(np.arange(0,dwaMin.time_array.shape[0]), dwaMin.time_array-dwaRobust.time_array, c="red", s = 100)
    ax4.scatter(np.arange(0,dwaMax.time_array.shape[0]), dwaMax.time_array-dwaRobust.time_array, c="blue", s = 100)
    ax4.plot([0,14], [0,0],"blue", linestyle='dashed')

    print
    print "print raw path length data"
    print "A:",  dwaStop.array
    print "B:",  dwaMin.array
    print "C:",  dwaMax.array
    print "D:",  dwaRobust.array
    print "E:",  dwaMinOnly.array
    print "F:",  dwaMaxOnly.array

    print
    print "print raw time data"
    print "A:",  dwaStop. time_array
    print "B:",  dwaMin. time_array
    print "C:",  dwaMax. time_array
    print "D:",  dwaRobust. time_array
    print "E:",  dwaMinOnly. time_array
    print "F:",  dwaMaxOnly. time_array


    plt.show()
