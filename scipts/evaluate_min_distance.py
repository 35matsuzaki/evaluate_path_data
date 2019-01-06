#!/usr/bin/python
# coding: UTF-8
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import sys

A_passing = [55,56,57,62,63,64]
A_crossing = [58,59,60,61,65,66,67,68,69,70,71]
A_random =[72,73,74]
B_passing = [37,38,39,44,46,47]
B_crossing = [40,41,42,43,48,49,50,51,52,53,54]
B_random =[55,56,57]
C_passing = [16,17,18,23,24,26]
C_crossing = [19,20,21,22,27,28,29,30,31,32,33]
C_random =[34,35,36]
D_passing = [35,36,37,42,43,44]
D_crossing = [38,39,40,41,45,46,47,48,49,50,51]
D_random =[52,53,54]

TIME_ROW = 0
X_ROW = 1
Y_ROW = 2
X_MAX_ = 16.0
X_MIN_ = -9.0

class PlotPotential:
    def __init__(self):
        # self.dir_name = dir_name
        self.SIZE = 10
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(221) #左上
        self.ax2 = self.fig.add_subplot(222) #右上
        self.ax3 = self.fig.add_subplot(223) #左下
        self.ax4 = self.fig.add_subplot(224) #右下
        self.actor_data = []
        self.robot_data = []

        self.hz = 10 # 0 or 10
        self.A_hist_result = np.array([])
        self.B_hist_result = np.array([])
        self.C_hist_result = np.array([])
        self.D_hist_result = np.array([])
        self.x_min = -10 #-10
        self.x_max = 12 # 12
        self.y_min = -4 # -4
        self.y_max = 4 #4
        self.z_min = 0.0
        self.z_max = 1.3 # exp:1, linear:30
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
            time = np.append(time,data[i][TIME_ROW])
            x = np.append(x,data[i][X_ROW])
            y = np.append(y,data[i][Y_ROW])
        return [time,x,y]

    def setData(self, dir_name):
        for file in os.listdir(dir_name):
            #csvファイルを読み込む
            file_path = dir_name + "/" + file
            data = self.readCsv(file_path)

            #ロボットの軌跡ファイル以外に対して
            if not "robot" in file:
                self.actor_data.append(data)
            else:
                self.robot_data = data


    def run(self):
        # self.ax1.cla()
        # self.ax2.cla()

        # min_dist = 100
        min_dist = np.array([])
        end_index=np.argmin(np.abs(self.robot_data[1]-X_MAX_))
        start_index=np.argmin(np.abs(self.robot_data[1]-X_MIN_))
        # print start_index,end_index

        for count in range(start_index, end_index+1, self.hz):
            current_time = self.robot_data[0][count]
            current_robot = [self.robot_data[1][count],self.robot_data[2][count]]
            # print current_robot

            for i in range(len(self.actor_data)):
                tmp_actor = np.array(self.actor_data[i])
                time_index = np.argmin(np.abs(tmp_actor[0][:]-current_time))
                # print tmp_actor[0][time_index],current_time
                current_actor = [tmp_actor[1][time_index], tmp_actor[2][time_index]]
                tmp_dist =np.sqrt((current_actor[0]-current_robot[0])**2 + (current_actor[1]-current_robot[1])**2)

                if tmp_dist < 3.0:
                    min_dist = np.append(min_dist, tmp_dist)
                # if min_dist > tmp_dist:
                    # min_dist = tmp_dist


        return min_dist

    def plotHist(self):
        # self.ax1.hist(self.A_hist_result, range=(self.z_min, self.z_max))
        self.ax2.hist(self.B_hist_result, range=(self.z_min, self.z_max))
        self.ax3.hist(self.C_hist_result, range=(self.z_min, self.z_max))
        self.ax4.hist(self.D_hist_result, bins = np.arange(0.6,1.8, 0.3),align="left") #, range=(self.z_min, self.z_max)
        #self.ax1.hist([self.A_hist_result,self.B_hist_result,self.C_hist_result,self.D_hist_result],color=['black','red', 'blue', 'green'], range=(self.z_min, self.z_max), bins = 5)
        self.ax1.hist([self.A_hist_result,self.B_hist_result,self.C_hist_result,self.D_hist_result],color=['black','red', 'blue', 'green'], bins = np.arange(0.6,1.8, 0.3),align="left")
        #self.ax1.plot([1.1, 1.1],[0, 250], "red", linestyle='dashed')
        self.ax1.set_xticks([0.6, 0.9, 1.2, 1.5])
        tmp = 200
        self.ax1.set_xlim(0.4,1.7)
        # self.ax2.set_ylim(0,tmp)
        # self.ax3.set_ylim(0,tmp)
        # self.ax4.set_ylim(0,tmp)
        plt.show()

    def clean(self):
        self.actor_data = []
        self.robot_data = []
    def printResult(self):
        print "Max:    A    B    C    D"
        print "    ", np.average(self.A_hist_result),np.average(self.B_hist_result),np.average(self.C_hist_result),np.average(self.D_hist_result)


if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2:
        print "usage: $python %s <target_dir>" % args[0]
        print "usage: arg[1] = tome result dir (i.e ./tome/all)"
        exit()
    dir_name = args[1]

    # #出力用のディレクトリを作成する
    # if not os.path.isdir(args[4]):
    #     os.mkdir(args[4])


    pltPote = PlotPotential()
    # pltPote.setData(dir_name)

    for tmp_dir in os.listdir(dir_name):
        target = os.path.join(dir_name, tmp_dir)
        print target

        pltPote.clean()
        pltPote.setData(target)
        tmp_cost = pltPote.run()
        policy = tmp_dir.split("_")[-1]
        if policy == "A5":
            pltPote.A_hist_result = np.append(pltPote.A_hist_result, tmp_cost)
        if policy == "E5":
            pltPote.B_hist_result = np.append(pltPote.B_hist_result, tmp_cost)
        if policy == "F5":
            pltPote.C_hist_result = np.append(pltPote.C_hist_result, tmp_cost)
        if policy == "I5":
            pltPote.D_hist_result = np.append(pltPote.D_hist_result, tmp_cost)


    pltPote.plotHist()
    pltPote.printResult()
    # ani = animation.FuncAnimation(pltPote.fig, pltPote.run, interval=10,frames=280)

    # for tmp_dir in os.listdir(dir_name):
    #     target = dir_name + "/" + tmp_dir
    #     for files in os.listdir(target):
    #         filename = target + "/" + files
    #         if files.split("/")[-1].split("-")[0] != "robot" and files.split("/")[-1].split("_")[0] != "robot":
    #             continue
    #
    #         data = pltPote.readCsv(filename)
    #         plt.plot(data[1][:],data[2][:])

    # plt.show()

    #plt.savefig("tmp.png")
