import pandas as pd


class Data:

    """
        values 0:零件号
               1:零件名
               2:供应商号
               5:提货点地址
               10:包装长
               11:包装宽
               12:包装高
               13:装箱数/包装
               14:每车用量
               16:频数


        pos 0:供应商编号
            2:经度
            3:维度
    """

    # 从excel文件读取并保存在一个二维数组
    def __init__(self):

        # 获取案例12原始数据

        input_file1 = '12.xls'
        df = pd.read_excel(input_file1, sheet_name=0)
        self.values = df.values

        # 获取所有供应商地址数据

        input_file2 = 'position.xlsx'
        df = pd.read_excel(input_file2, sheet_name=0)
        self.pos = df.values

    # 返回供应商坐标和产品信息
    def get_info(self):

        # x 经度 y 纬度
        x = []
        y = []
        info = []
        for i in range(len(self.pos)):
            x.append(self.pos[i, 2])
            y.append(self.pos[i, 3])
            tmp = []
            for j in range(len(self.values)):
                if self.pos[i, 0] == self.values[j, 2]:
                    tmp2 = list()
                    tmp2.append(self.values[j, 0])
                    tmp2.append(int(self.values[j, 10]))
                    tmp2.append(int(self.values[j, 11]))
                    tmp2.append(int(self.values[j, 12]))
                    tmp2.append(int(self.values[j, 13]))
                    tmp2.append(int(self.values[j, 14]))
                    tmp2.append(int(self.values[j, 16]))
                    tmp.append(tmp2)
            info.append(tmp)

        # info 第一维供应商 第二维对应零件集合
        #      第三维零件信息 0 零件号 1 长 2 宽 3 高 4 装箱数 5 每车用量 6 频数
        return x, y, info


# test code

# my_data = Data()
# print(my_data.values)
# a = []
# for i in range(len(my_data.values)):
#     a1 = int(my_data.values[i, 10])
#     a2 = int(my_data.values[i, 11])
#     a3 = int(my_data.values[i, 12])
#     a.append(a1 * a2 * a3 / 1000)
#
# a = set(a)
# print(a)
# print(len(a))
# 620种体积的箱子
# print(f)
# print(len(set(f)))
# print(my_data.pos)
# x, y, info = my_data.get_info()
# print(x)
# print(y)
# print(info)
