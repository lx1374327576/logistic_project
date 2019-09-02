import data
import result
import math
import numpy as np


# 问题解决框架
class Solver:

    def __init__(self, car_x=12, car_y=2.35, car_z=2.5, car_coe=0.9, machine_x=None, machine_y=None, car_num=600,
                 pro_num=192):
        """
        :param car_x: 单个小卡车长
        :param car_y: 单个小卡车宽
        :param car_z: 单个小卡车高 选取了一种常用尺寸
        :param car_coe: 容量安全系数
        :param machine_x: 主机厂经度
        :param machine_y: 主机厂纬度 如没有按照平均计算
        :param car_num: 平均车的日产量 年产量除以三百天计算
        :param pro_num: 供应商数量

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

    # 传统运输方式 简单体积 以里程为代价 不管频次/时间窗
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

    # 节约里程法 简单体积 以里程为代价 不管频次/时间窗
    def get_saveDis_simpleV_mileageCost_noFre(self):

        total_dis_tmp = 0
        total_car_fre = 0
        per_car = self.car_x * self.car_y * self.car_z * self.car_coe

        left = []
        for i in range(self.pro_num):
            dis = self.my_data.get_dis(x1=self.machine_x, y1=self.machine_y, x2=self.x[i], y2=self.y[i])
            now_set = self.info[i]
            total_v = 0
            for part in now_set:
                total_v += part[1] / 1000 * part[2] / 1000 * part[3] / 1000 * self.car_num * part[5] / part[4]
            total_car_fre += math.floor(total_v / per_car)
            left.append(total_v - math.floor(total_v / per_car) * per_car)
            total_dis_tmp += dis * 2 * math.floor(total_v / per_car)
        mid_dis = total_dis_tmp

        tag = []
        for i in range(self.pro_num):
            tag.append(0)
        for i in range(self.pro_num):
            max_v = 0
            now = -1
            tmp_v = per_car
            for j in range(self.pro_num):
                if tag[j] == 0 and left[j] > max_v:
                    now = j
                    max_v = left[j]
            if now == -1:
                break

            tmp_v -= max_v
            left[now] = 0
            tag[now] = 1
            tmp_dis = self.my_data.get_dis(x1=self.machine_x, y1=self.machine_y, x2=self.x[now], y2=self.y[now])
            # pri = []
            # pri.append(tmp_dis)
            while tmp_v > 0:
                min_d = 100000000000
                now_tmp = -1
                for j in range(self.pro_num):
                    if tag[j] == 0 and self.dis[now][j] < min_d and tmp_v >= left[j]:
                        now_tmp = j
                        min_d = self.dis[now][j]
                if now_tmp == -1:
                    break
                tmp_dis += min_d
                # pri.append(min_d)
                if left[now_tmp] > tmp_v:
                    tmp_v = 0
                    left[now_tmp] -= tmp_v
                else:
                    tmp_v -= left[now_tmp]
                    left[now_tmp] = 0
                    tag[now_tmp] = 1
                now = now_tmp
            tmp_dis += self.my_data.get_dis(x1=self.machine_x, y1=self.machine_y, x2=self.x[now], y2=self.y[now])
            # pri.append(self.my_data.get_dis(x1=self.machine_x, y1=self.machine_y, x2=self.x[now], y2=self.y[now]))
            # print(pri)
            total_dis_tmp += tmp_dis
            total_car_fre += 1

        res = result.Result()
        res.total_dis = total_dis_tmp
        res.total_car_fre = total_car_fre
        res.mid_dis = mid_dis
        return res

    # 节约里程法 简单体积 以里程为代价 管频次/时间窗
    def get_saveDis_simpleV_mileageCost_Fre(self):

        # 设定货车出发时间 0点 工作时间点（8-17） 8 12 10 14 11 9
        # 设定平均装货时间 12分钟/供应商 货车平均时速 60km/h
        avg_v = 60
        avg_loading_time = 0.333333
        duetime_point = [8, 9, 10, 11, 12, 14]
        duetime_map = [[0], [0, 4], [0, 2, 4], [0, 2, 4, 5], [0, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5]]
        start_point = 0
        car_plan = []
        plan_timezone = []
        plan_timepoint = []
        total_dis_tmp = 0
        total_car_fre = 0

        # 按简单体积分割每个供应商的产品和时间
        left = []
        for i in range(self.pro_num):
            tmp_per_left = [0, 0, 0, 0, 0, 0]
            now_set = self.info[i]
            for part in now_set:
                for j in range(part[6]):
                    tmp_per_left[duetime_map[part[6]-1][j]] += self.car_num * part[5] * part[1] / 1000 * part[2] / 1000\
                                        * part[3] / 1000 / part[4] / part[6]
            left.append(tmp_per_left)
        # print(left)

        # 一部分直送 直接剔除
        per_car = self.car_x * self.car_y * self.car_z * self.car_coe
        for i in range(self.pro_num):
            sum_v = np.sum(left[i])
            per_car_number = math.floor(sum_v / per_car)
            car_route = [i]
            for j in range(per_car_number):
                car_plan.append(car_route)
                time_tmp = self.my_data.get_dis(x1=self.machine_x, y1=self.machine_y, x2=self.x[i],
                                                y2=self.y[i]) / avg_v
                plan_timezone.append(2 * (time_tmp + avg_loading_time))
                plan_timepoint.append([time_tmp, 2*time_tmp + avg_loading_time])
            total_car_fre += per_car_number
            total_dis_tmp += 2 * per_car_number * self.my_data.get_dis(x1=self.machine_x, y1=self.machine_y,
                                                                       x2=self.x[i], y2=self.y[i])
            tmp_v = per_car_number * per_car
            for j in range(6):
                if tmp_v >= left[i][j]:
                    tmp_v -= left[i][j]
                    left[i][j] = 0
                else:
                    left[i][j] -= tmp_v
                    tmp_v = 0
        mid_dis = total_dis_tmp
        # print(mid_dis)

        # print(left)

        # 可以进行精细装填 剔除高体积部分

        # 可以进行聚类

        # 按照符合时间的节约里程法进行贪心
        per_car = self.car_x * self.car_y * self.car_z * self.car_coe
        # t数组表示该边是否可行 0可行 1不可行
        t = []
        for i in range(self.pro_num):
            tmp_t = []
            for j in range(self.pro_num):
                d1 = self.my_data.get_dis(x1=self.machine_x, y1=self.machine_y, x2=self.x[i], y2=self.y[i])
                d2 = self.my_data.get_dis(x1=self.machine_x, y1=self.machine_y, x2=self.x[j], y2=self.y[j])
                if d1 + d2 > self.dis[i][j]:
                    tmp_t.append(0)
                else:
                    tmp_t.append(1)
            t.append(tmp_t)

        tag = []
        for i in range(self.pro_num):
            tag.append([0, 1, 1, 1, 1, 1])
            left[i][0] = np.sum(left[i])

        # print(tag)
        for i in range(self.pro_num):
            # 初始化
            tmp_v = per_car
            tmp_time = avg_loading_time
            tmp_dis = 0
            plan = []
            tmp_plan_timepoint = []
            # 选最大的
            max_v = 0
            min_dis_point_j = -1
            min_dis_point_k = -1
            for j in range(self.pro_num):
                for k in range(6):
                    if tag[j][k] == 0 and left[j][k] > max_v:
                        max_v = left[j][k]
                        min_dis_point_j = j
                        min_dis_point_k = k
            if min_dis_point_j == -1:
                break
            tmp_time += self.my_data.get_dis(x1=self.machine_x, y1=self.machine_y, x2=self.x[min_dis_point_j],
                                             y2=self.y[min_dis_point_j]) / avg_v + avg_loading_time
            tmp_plan_timepoint.append(tmp_time - 2 * avg_loading_time)
            tmp_v -= left[min_dis_point_j][min_dis_point_k]
            tag[min_dis_point_j][min_dis_point_k] = 1
            left[min_dis_point_j][min_dis_point_k] = 0
            plan.append(min_dis_point_j)
            tmp_dis += self.my_data.get_dis(x1=self.machine_x, y1=self.machine_y, x2=self.x[min_dis_point_j],
                                            y2=self.y[min_dis_point_j])

            # 不停的选最优的
            now_point = min_dis_point_j
            due_time = duetime_point[min_dis_point_k]
            while True:
                min_dis = 10000
                min_dis_point_j = -1
                min_dis_point_k = -1
                for j in range(self.pro_num):
                    for k in range(6):
                        if tag[j][k] == 0 and self.dis[now_point][j] < min_dis and t[now_point][j] > -1 and tmp_v > left[j][k]\
                            and due_time - start_point > tmp_time + avg_loading_time + self.dis[now_point][j] / avg_v\
                                + self.my_data.get_dis(x1=self.machine_x, y1=self.machine_y, x2=self.x[j], y2=self.y[j]) / avg_v:
                                    min_dis = self.dis[now_point][j]
                                    min_dis_point_j = j
                                    min_dis_point_k = k
                if min_dis_point_j == -1:
                    break
                tmp_time += min_dis / avg_v + avg_loading_time
                tmp_plan_timepoint.append(tmp_time - 2 * avg_loading_time)
                now_point = min_dis_point_j
                if duetime_point[min_dis_point_k] < due_time:
                    due_time = duetime_point[min_dis_point_k]
                tmp_v -= left[min_dis_point_j][min_dis_point_k]
                tag[min_dis_point_j][min_dis_point_k] = 1
                left[min_dis_point_j][min_dis_point_k] = 0
                plan.append(min_dis_point_j)
                tmp_dis += min_dis
            tmp_time += self.my_data.get_dis(x1=self.machine_x, y1=self.machine_y, x2=self.x[now_point],
                                             y2=self.y[now_point]) / avg_v
            tmp_plan_timepoint.append(tmp_time - avg_loading_time)
            tmp_dis += self.my_data.get_dis(x1=self.machine_x, y1=self.machine_y, x2=self.x[now_point],
                                            y2=self.y[now_point])
            # print(tmp_dis)
            total_dis_tmp += tmp_dis
            total_car_fre += 1
            car_plan.append(plan)
            plan_timezone.append(tmp_time)
            plan_timepoint.append(tmp_plan_timepoint)

        # print(tag)
        # print(car_plan)
        # 返回运行结果
        res = result.Result()
        res.total_dis = total_dis_tmp
        res.total_car_fre = total_car_fre
        res.mid_dis = mid_dis
        res.car_plan = car_plan
        res.plan_timezone = plan_timezone
        res.plan_timepoint = plan_timepoint
        return res

    # 节约里程库存法 简单体积 以里程和库存为代价(不允许缺货) 管频次/时间窗
    def get_saveDisSto_simpleV_mileageStockCost_Fre(self):

        # 设定货车出发时间 0点 工作时间点（8-17） 8 12 10 14 11 9
        # 设定平均装货时间 体积/总体积*0.5h 货车平均时速 60km/h
        avg_v = 60
        avg_loading_time = 0.5
        pass


# test code

# test for get_trad_simpleV_mileageCost_noFre get_saveDis_simpleV_mileageCost_noFre
sol = Solver()
res1 = sol.get_trad_simpleV_mileageCost_noFre()
print('传统算法', res1.total_dis)
# print(res.total_car_fre)
res2 = sol.get_saveDis_simpleV_mileageCost_noFre()
print('节约里程法', res2.total_dis)
# print('节约百分数', (res1.total_dis-res2.total_dis)/res1.total_dis)
# print('实际节约百分数', (res1.total_dis-res2.total_dis)/(res1.total_dis - res2.mid_dis))
# print(res.total_car_fre)
#
# test for get_saveDis_simpleV_mileageCost_Fre
# sol = Solver()
res3 = sol.get_saveDis_simpleV_mileageCost_Fre()
print('节约里程法（考虑时间）', res3.total_dis)
# print('节约百分数', (res1.total_dis-res3.total_dis)/res1.total_dis)
# print('较传统实际节约百分数', (res1.total_dis-res3.total_dis)/(res1.total_dis - res3.mid_dis))
# print('较节约里程法实际节约百分数', (res2.total_dis-res3.total_dis)/(res2.total_dis - res3.mid_dis))
# print(res3.total_car_fre)
