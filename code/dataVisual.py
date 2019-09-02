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


# test code
# worker = DataVisual()
# my_data = data.Data()
# sol = solver.Solver()
# x, y, _, _ = my_data.get_info()
# worker.draw_scatter(x, y, sol.machine_x, sol.machine_y)
