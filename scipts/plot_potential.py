#!/usr/bin/python
# coding: UTF-8
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import sys


class PlotPotential:
    def __init__(self, dir_name):
        self.dir_name = dir_name
        self.SIZE = 10
        self.var = 1
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(211)
        self.ax2 = self.fig.add_subplot(212)
        self.actor_data = []
        self.robot_data = []

        self.hz = 10 #0:10hz, 10:100hz
        self.hist_result = np.array([])
        self.x_min = -10 #-10
        self.x_max = 12 # 12
        self.y_min = -4 # -4
        self.y_max = 4 #4
        self.z_min = 0
        self.z_max = 1 # exp:1, linear:30
        self.grid_width = 0.1
        self.x_grid_width = (self.x_max-self.x_min)/self.grid_width
        self.y_grid_width = (self.y_max-self.y_min)/self.grid_width
        self.area = [self.x_min, self.x_max, self.y_min,self.y_max]
        self.side_x = np.linspace(self.x_min, self.x_max, self.x_grid_width)
        self.side_y = np.linspace(self.y_min, self.y_max, self.y_grid_width)
        self.x_variable, self.y_variable =  np.meshgrid(self.side_x, self.side_y)

        self.traj_cost = 0
        self.tmp = 0 #for debug, output result
    def readCsv(self, filename):
        data = np.genfromtxt(filename, delimiter=',')
        time = np.array([])
        x = np.array([])
        y = np.array([])
        value = np.array([])
        for i in range(len(data)):
            time = np.append(time,data[i][0])
            x = np.append(x,data[i][1])
            y = np.append(y,data[i][2])
        return [time,x,y]

    def setData(self):
        for file in os.listdir(self.dir_name):
            #csvファイルを読み込む
            file_path = self.dir_name + "/" + file
            data = self.readCsv(file_path)

            #ロボットの軌跡ファイル以外に対して
            if file_path.split("/")[-1].split("-")[0] != "robot" and file_path.split("/")[-1].split("_")[0] != "robot":
                self.actor_data.append(data)
            else:
                self.robot_data = data


    def run(self, count):
        self.ax1.cla()
        self.ax2.cla()

        current_time = self.robot_data[0][count+self.hz]


        for i in range(len(self.actor_data)):
            tmp_actor = np.array(self.actor_data[i])
            time_index = np.argmin(np.abs(tmp_actor[0][:]-current_time))
            # print tmp_actor[0][time_index],current_time
            current_actor = [tmp_actor[1][time_index], tmp_actor[2][time_index]]
            # print "pose:",current_actor
            self.ax1.plot(current_actor[0], current_actor[1], "ko", ms= self.SIZE)
            if i == 0:
                z_value = np.exp(-((self.x_variable-current_actor[0])**2+(self.y_variable-current_actor[1])**2)/self.var)
                # z_value = np.sqrt((self.x_variable-current_actor[0])**2+(self.y_variable-current_actor[1])**2)

            else:
                z_value = z_value + np.exp(-((self.x_variable-current_actor[0])**2+(self.y_variable-current_actor[1])**2)/self.var)
                # z_value = z_value + np.sqrt((self.x_variable-current_actor[0])**2+(self.y_variable-current_actor[1])**2)

        # print z_value.shape # (y, x):(80, 220)
        cuurent_robot = [self.robot_data[1][count+self.hz], self.robot_data[2][count+self.hz]]
    #    z_value = np.exp(-((self.x_variable-cuurent_robot[0])**2+(self.y_variable-cuurent_robot[1])**2))
        current_cost = z_value[int((cuurent_robot[1] - self.y_min)/self.grid_width),int((cuurent_robot[0] - self.x_min)/self.grid_width)]
        self.traj_cost = self.traj_cost + current_cost
        print self.traj_cost, current_cost
        self.hist_result = np.append( self.hist_result, current_cost)

        self.tmp = z_value

        self.ax1.pcolormesh(self.x_variable,self.y_variable,z_value, vmin=self.z_min, vmax=self.z_max)
        self.ax1.plot(cuurent_robot[0], cuurent_robot[1], "wo", ms= self.SIZE)
        self.ax1.set_aspect('equal', adjustable='box')
        self.ax1.axis(self.area)

        self.ax2.hist(self.hist_result, range=(self.z_min, self.z_max))
        self.ax2.set_ylim(0,200)

if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2:
        print "usage: $python %s <target_dir>" % args[0]
        exit()
    dir_name = args[1]

    # #出力用のディレクトリを作成する
    # if not os.path.isdir(args[4]):
    #     os.mkdir(args[4])

    pltPote = PlotPotential(dir_name)
    pltPote.setData()

    # for i in range(200):
        # pltPote.run(i)
        # input = raw_input()
        # if input == "p":
        #     print tmp
        #     np.savetxt("test.csv", tmp, delimiter=",", fmt="%s")
        #     break
        # else:
        #     plt.pause(0.1)
        # plt.pause(0.1)

    ani = animation.FuncAnimation(pltPote.fig, pltPote.run, interval=10,frames=280)
    plt.show()

    #plt.savefig("tmp.png")
