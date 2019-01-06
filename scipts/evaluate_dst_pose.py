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
FILE_NAME = "_slash_dst_pose.csv"
X_ROW = 16
Y_ROW = 17
Z_ROW = 18
X_MAX = 17.0
X_MIN = 2.0
SECS_ROW = 4
NSECS_ROW = 5
OFFSET = 30

if len(argvs) != 2:
    print "usage python %s <target dir>" % argvs[0]
    exit()


def readCsv(filename):
    print filename
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
        self.label0 = np.array([])
        self.label1 = np.array([])
        self.label2 = np.array([])


if __name__ == "__main__":
    target_dir = argvs[1]

    dwaStop = Policy("k",".")

    for dir in sorted(os.listdir(target_dir)):
        data = readCsv(target_dir + "/" + dir+ "/" + FILE_NAME)
        # print data.shape
        dst_raw_result = data[1:,X_ROW:Z_ROW+1].astype(np.float)
        # print dst_raw_result.shape
        # secs_list = data[1:, SECS_ROW]
        # nsecs_list = data[1:, NSECS_ROW]

        count = 0
        for current_dst in dst_raw_result:
            count = count + 1
            if count < OFFSET:
                continue
            if count > dst_raw_result.shape[0] - OFFSET:
                break

            expSum = np.sum(np.exp(current_dst))
            current_dst = (np.exp(current_dst))/expSum
            # print current_dst
            maxIndex = np.argmax(current_dst)
            
            if maxIndex == 0:
                dwaStop.label0 = np.append(dwaStop.label0, np.array([current_dst[0]]))
            if maxIndex == 1:
                dwaStop.label1 = np.append(dwaStop.label1, np.array([current_dst[1]]))
            if maxIndex == 2:
                dwaStop.label2 = np.append(dwaStop.label2, np.array([current_dst[2]]))
            # if current_dst[0] < 0.05:
                # dwaStop.count = dwaStop.count + 1

    ax.hist(dwaStop.label1)
    # print dwaStop.label0.shape
    # print dwaStop.label1.shape
    # print dwaStop.label2.shape
    plt.show()
