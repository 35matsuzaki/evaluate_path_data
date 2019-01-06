#!/usr/bin/python
# coding: UTF-8
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import sys

argvs = sys.argv
if len(argvs) != 2:
    print "usage python %s <target dir>" % argvs[0]
    exit()


def readCsv(filename):
    data = np.genfromtxt(filename, delimiter=',')
    time = np.array([])
    x = np.array([])
    y = np.array([])
    value = np.array([])
    for i in range(len(data)):
        time = np.append(time,data[i][0])
        x = np.append(x,data[i][1])
    return [time,x]


if __name__=="__main__":
    target_dir = argvs[1] #
    for dir in sorted(os.listdir(target_dir)): #1-10
        tmp_dir = target_dir + "/" + dir
        for file in sorted(os.listdir(tmp_dir)): #pede, robot
            file_path = tmp_dir + "/" + file
            data =readCsv(file_path)
            print file_path, data[0].shape[0]
            if data[0].shape[0] < 80:
                os.remove(file_path)
