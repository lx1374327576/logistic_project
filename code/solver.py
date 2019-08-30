import data
import result
import math


# 问题解决框架
class Solver:

    def __init__(self, car_x=12, car_y=2.35, car_z=2.5, car_coe=0.9, machine_x=None, machine_y=None, car_num=600,
                 pro_num=192, mode='traditional'):
        """
        :param car_x: 单个小卡车长
        :param car_y: 单个小卡车宽
        :param car_z: 单个小卡车高 选取了一种常用尺寸
        :param car_coe: 容量安全系数
        :param machine_x: 主机厂经度
        :param machine_y: 主机厂纬度 如没有按照平均计算
        :param car_num: 平均车的日产量 年产量除以三百天计算
        :param pro_num: 供应商数量
        :param mode: 指定方案解决模式

        """

        # 提取excel信息
        my_data = data.Data()
        x, y, dis, info = my_data.get_info()
        self.my_data = my_data
        self.x = x
        self.y = y
        self.dis = dis
        self.info = info

        self.car_x = car_x
        self.car_y = car_y
        self.car_z = car_z
        self.car_coe = car_coe
        self.pro_num = pro_num
        self.mode = mode
        self.car_num = car_num

        if machine_x is None:
            tmp = 0
            for i in range(pro_num):
                tmp += x[i]
            self.machine_x = tmp / pro_num
        else:
            self.machine_x = machine_x

        if machine_y is None:
            tmp = 0
            for i in range(pro_num):
                tmp += y[i]
            self.machine_y = tmp / pro_num
        else:
            self.machine_y = machine_x

    # 传统运输方式 简单体积 以里程为代价 不管频次
    def get_trad_simpleV_mileageCost_noFre(self):

        total_dis_tmp = 0
        total_car_fre = 0
        for i in range(self.pro_num):
            dis = self.my_data.get_dis(x1=self.machine_x, y1=self.machine_y, x2=self.x[i], y2=self.y[i])
            now_set = self.info[i]
            total_v = 0
            for part in now_set:
                total_v += part[1]/1000 * part[2]/1000 * part[3]/1000 * self.car_num * part[5] / part[4]
            total_car_fre += math.ceil(total_v / (self.car_x * self.car_y * self.car_z * self.car_coe))
            total_dis_tmp += dis * 2 * math.ceil(total_v / (self.car_x * self.car_y * self.car_z * self.car_coe))
            # print('test', i, total_v)
            # if i == 191:
            #     print(now_set)

        res = result.Result()
        res.total_dis = total_dis_tmp
        res.total_car_fre = total_car_fre
        return res


# test code
# sol = Solver()
# res = sol.get_trad_simpleV_mileageCost_noFre()
# print(res.total_dis)
# print(res.total_car_fre)

