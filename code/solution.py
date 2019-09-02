import math
import data
import result


class Solution:

    def __init__(self, res, dat):
        """
        :param res:必须是result.Result类 用来存放求解结果
        :param dat:必须是data.Data类 用来存放原始数据

        """
        self.res = res
        self.data = dat

    # 根据求解方案 生成合适的派车方案
    def sol_balance_mileageCost(self):
        car_plan = self.res.car_plan
        plan_timezone = self.res.plan_timezone
        plan_timepoint = self.res.plan_timepoint
        pass

    # 向excel输出列车时刻表
    def print_to_excel(self, file_name):
        pass
