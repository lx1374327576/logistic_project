import matplotlib.pyplot as plt
import data
import solver
import numpy as np


class DataVisual:

    def __init__(self):
        pass

    def draw_scatter(self, x, y, main_x, main_y):

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.set_title('provider scatter picture')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.scatter(x, y, marker='.')
        ax.scatter(main_x, main_y, marker='x', s=50)
        plt.xlim(xmax=np.max(x)+0.1, xmin=np.min(x)-0.1)
        plt.ylim(ymax=np.max(y)+0.1, ymin=np.min(y)-0.1)
        plt.show()

    def draw_carNum(self):
        percent = []
        car_num = 600
        for i in range(11):
            percent.append(int(((i - 5) / 10 + 1) * car_num))
        total_dis1 = []
        total_price1 = []
        total_dis2 = []
        total_price2 = []
        total_dis3 = []
        for pc in percent:
            sol = solver.Solver(car_num=pc)
            res1 = sol.get_saveDisSto_simpleV_mileageStockCost_Fre()
            res2 = sol.get_saveDis_simpleV_mileageCost_Fre()
            res3 = sol.get_trad_simpleV_mileageCost_noFre()
            total_dis1.append(res1.total_dis)
            total_price1.append(res1.total_price)
            total_dis2.append(res2.total_dis)
            total_price2.append(res2.total_price)
            total_dis3.append(res3.total_dis)
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(1, 1, 1)
        ax1.set_title('harvest-distance picture')
        ax1.set_xlabel('vehicle')
        ax1.set_ylabel('km')
        ax1.plot(percent, total_dis1)
        ax1.plot(percent, total_dis2)
        ax1.plot(percent, total_dis3)
        fig2 = plt.figure()
        ax2 = fig2.add_subplot(1, 1, 1)
        ax2.set_title('harvest-price picture')
        ax2.set_xlabel('vehicle')
        ax2.set_ylabel('yuan')
        ax2.plot(percent, total_price1)
        ax2.plot(percent, total_price2)
        plt.show()


# test code

# test for draw_scatter
# worker = DataVisual()
# my_data = data.Data()
# sol = solver.Solver()
# x, y, _, _ = my_data.get_info()
# worker.draw_scatter(x, y, sol.machine_x, sol.machine_y)

# test for draw_carNum
worker = DataVisual()
worker.draw_carNum()
