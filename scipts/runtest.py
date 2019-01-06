#!/usr/bin/python
# coding: UTF-8
import plot_potential
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import sys

args = sys.argv
if len(args) != 2:
    print "usage: $python %s <target_dir>" % args[0]
    exit()
dir_name = args[1]

pltPote = plot_potential.PlotPotential(dir_name)
pltPote.setData()

ani = animation.FuncAnimation(pltPote.fig, pltPote.run, interval=10,frames=280)
plt.show()
