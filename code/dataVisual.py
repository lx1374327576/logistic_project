import matplotlib.pyplot as plt
import data
import solver
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


class DataVisual:

    def __init__(self):
        pass

    def draw_scatter(self):

        my_data = data.Data()
        sol = solver.Solver()
        sol.get_saveDis_simpleV_mileageCost_Fre()
        left = sol.left
        max_left = 0
        for i in range(len(left)):
            if np.sum(left[i]) > max_left:
                max_left = np.sum(left[i])
        max_left = max_left / 20
        color = []
        for i in range(len(left)):
            color.append(int(min(np.sqrt(np.sum(left[i]) / max_left), 1) * 19))
        print(color)
        main_x = sol.machine_x
        main_y = sol.machine_y
        x, y, _, _ = my_data.get_info()
        cm = plt.cm.get_cmap('RdYlBu')
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.set_title('provider scatter picture')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.scatter(x, y, marker='.', c=color, cmap=cm, label='provider')
        ax.scatter(main_x, main_y, marker='x', s=50, label='center')
        plt.xlim(xmax=np.max(x)+0.1, xmin=np.min(x)-0.1)
        plt.ylim(ymax=np.max(y)+0.1, ymin=np.min(y)-0.1)
        plt.legend()
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
        ax1.plot(percent, total_dis1, label='storage and distance')
        ax1.plot(percent, total_dis2, label='only distance')
        ax1.plot(percent, total_dis3, label='traditional')
        fig1.legend()
        fig2 = plt.figure()
        ax2 = fig2.add_subplot(1, 1, 1)
        ax2.set_title('harvest-price picture')
        ax2.set_xlabel('vehicle')
        ax2.set_ylabel('yuan')
        ax2.plot(percent, total_price1, label='storage and distance')
        ax2.plot(percent, total_price2, label='only distance')
        fig2.legend()
        plt.show()

    def draw_carType(self):
        vv = [26.42, 54.79, 68.36, 70.5, 85.79]
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.set_xlabel('v/m^3')
        ax.set_ylabel('price/yuan')
        ax.set_title('cartype-price picture')
        y = []
        for v in vv:
            sol = solver.Solver(car_x=v, car_y=1, car_z=1)
            res = sol.get_saveDisSto_simpleV_mileageStockCost_Fre(disPrice_coe=5.2*v/70.5)
            y.append(res.total_price)
        ax.plot(vv, y, label='car_type')
        plt.legend()
        plt.show()

    def draw_carType_new(self):
        vv = [26.42, 54.79, 68.36, 70.5, 85.79]
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.set_xlabel('v/m^3')
        ax.set_ylabel('distance/km')
        ax.set_title('cartype-distance picture')
        y = []
        for v in vv:
            sol = solver.Solver(car_x=v, car_y=1, car_z=1)
            res = sol.get_saveDisSto_simpleV_mileageStockCost_Fre(disPrice_coe=5.2*v/70.5)
            y.append(res.total_dis)
        ax.plot(vv, y, label='car_type')
        plt.legend()
        plt.show()

    def draw_carV(self):
        avg_v = 60
        percent = []
        for i in range(11):
            percent.append(int(((i - 5) / 10 + 1) * avg_v))
        sol = solver.Solver()
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.set_xlabel('v/m*s^-2')
        ax.set_ylabel('price/yuan')
        ax.set_title('carV-price picture')
        y = []
        for pc in percent:
            res = sol.get_saveDisSto_simpleV_mileageStockCost_Fre(avg_v=pc)
            y.append(res.total_price)
        ax.plot(percent, y, label='the v of car')
        plt.legend()
        plt.show()

    def draw_carV_new(self):
        avg_v = 60
        percent = []
        for i in range(11):
            percent.append(int(((i - 5) / 10 + 1) * avg_v))
        sol = solver.Solver()
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.set_xlabel('v/m*s^-2')
        ax.set_ylabel('distance/km')
        ax.set_title('carV-distance picture')
        y = []
        for pc in percent:
            res = sol.get_saveDisSto_simpleV_mileageStockCost_Fre(avg_v=pc)
            y.append(res.total_dis)
        ax.plot(percent, y, label='the v of car')
        plt.legend()
        plt.show()

    def draw_position(self):

        sol = solver.Solver()
        sol.get_saveDis_simpleV_mileageCost_Fre()
        main_x = sol.machine_x
        main_y = sol.machine_y
        X = np.arange(-0.5, 0.5, 0.1)
        Y = np.arange(-0.5, 0.5, 0.1)
        print(X)
        print(Y)
        X, Y = np.meshgrid(X, Y)
        print(main_x)
        print(main_y)
        Z = np.zeros_like(X)
        for i in range(len(X)):
            for j in range(len(X[i])):
                print(i, j)
                sol = solver.Solver(machine_x=main_x+X[i, j], machine_y=main_y+Y[i, j])
                res = sol.get_saveDisSto_simpleV_mileageStockCost_Fre()
                print(res.total_price)
                Z[i, j] = res.total_price
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='rainbow')
        plt.show()


# test code

# test for draw_scatter
# worker = DataVisual()
# worker.draw_scatter()

# test for draw_carNum
# worker = DataVisual()
# worker.draw_carNum()

# test for draw_carType
# worker = DataVisual()
# worker.draw_carType_new()

# test for draw_carV_new
# worker = DataVisual()
# worker.draw_carV_new()

# test for draw_position
worker = DataVisual()
worker.draw_position()
