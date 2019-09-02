import math
import data
import result
import solver


class Solution:

    def __init__(self, res, dat):
        """
        :param res:必须是result.Result类 用来存放求解结果
        :param dat:必须是data.Data类 用来存放原始数据

        """
        self.result = res
        self.data = dat
        self.car_plan = None

    def get_time(self, number):
        s = str(math.floor(number))
        left = number - math.floor(number)
        left = left * 60
        left = int(left)
        if left < 10:
            s = s + ':'+'0' + str(left)
        else:
            s = s + ':' + str(left)
        return s

    def get_name(self, rank):
        id_to_address = self.data.id_to_address
        if rank == -1:
            return '总厂'
        else:
            return id_to_address[rank][0].strip()

    def get_address(self, rank):
        id_to_address = self.data.id_to_address
        if rank == -1:
            return '安吉物流零部件'
        else:
            return id_to_address[rank][1].strip()

    # 根据求解方案 生成合适的派车方案
    def sol_balance_mileageCost(self):
        car_plan = self.result.car_plan
        for plan in car_plan:
            plan.append(-1)
        plan_timezone = self.result.plan_timezone
        plan_timepoint = self.result.plan_timepoint
        seq = []
        num = len(plan_timepoint)
        for i in range(num):
            seq.append(i)
        for i in range(num):
            min_time = 100
            min_pos = -1
            for j in range(i+1, num, 1):
                if plan_timezone[seq[j]] < min_time:
                    min_time = plan_timezone[seq[j]]
                    min_pos = j
            tmp = seq[i]
            seq[i] = seq[min_pos]
            seq[min_pos] = tmp

        mid_car_plan = []
        timezone = 8
        first = 0
        last = num - 1
        while first <= last:
            tmp_car_plan = []
            tmp_timezone = timezone
            tmp_car_plan.append(seq[last])
            tmp_timezone -= plan_timezone[seq[last]]
            last -= 1
            while first <= last and tmp_timezone > plan_timezone[seq[first]]:
                tmp_car_plan.append(seq[first])
                tmp_timezone -= plan_timezone[seq[first]]
                first += 1
            mid_car_plan.append(tmp_car_plan)

        final_car_plan = []
        num = len(mid_car_plan)
        for i in range(num):
            tmp_car_plan = []
            tmp_timezone = 0
            for j in mid_car_plan[i]:
                for k in range(len(plan_timepoint[j])):
                    tmp_car_plan.append([self.get_time(plan_timepoint[j][k] + tmp_timezone),
                                         self.get_name(car_plan[j][k]),
                                         self.get_address(car_plan[j][k])])
                tmp_timezone += plan_timezone[j]
            final_car_plan.append(tmp_car_plan)
        self.car_plan = final_car_plan

    # 向txt输出列车时刻表
    def print_to_txt(self, file_name):
        f = open(file_name, "w")
        num = len(self.car_plan)
        for i in range(num):
            for point in self.car_plan[i]:
                print(point[0], point[1], point[2], file=f)
            print('', file=f)
            print('------------------------------car ' + str(i+1) + '------------------------------', file=f)
            print('', file=f)


# test code
test_solver = solver.Solver()
test_data = data.Data()
test_result = test_solver.get_saveDis_simpleV_mileageCost_Fre()
test_solution = Solution(test_result, test_data)
# print(test_solution.result.plan_timezone)
test_solution.sol_balance_mileageCost()
test_solution.print_to_txt('car_solution.txt')
