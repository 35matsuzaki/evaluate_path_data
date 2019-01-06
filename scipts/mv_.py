#!/usr/bin/python
# coding: UTF-8
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import sys
import shutil

argvs = sys.argv
if len(argvs) != 2:
    print "usage python %s <target dir>" % argvs[0]
    exit()


if __name__=="__main__":
    target_dir = argvs[1] #
    for dir in sorted(os.listdir(target_dir)): #1-10
        tmp_dir = target_dir + "/" + dir
        output_path = target_dir + "_" + dir
        shutil.move(tmp_dir, output_path)
