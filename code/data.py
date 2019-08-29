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

    """

    # 从excel文件读取并保存在一个二维数组
    def __init__(self):

        # 获取案例12原始数据

        input_file1 = '12.xls'
        df = pd.read_excel(input_file1, sheet_name=0)
        self.values = df.values

        # 获取所有供应商地址数据

        input_file2 = 'position.xlsx'
        df = pd.read_excel(input_file1, sheet_name=0)
        self.pos = df.values


# test code
my_data = Data()
# print(my_data.values)
"""
a = []
for i in range(len(my_data.values)):
    a1 = int(my_data.values[i, 10])
    a2 = int(my_data.values[i, 11])
    a3 = int(my_data.values[i, 12])
    a.append(a1 * a2 * a3 / 1000)

a = set(a)
print(a)
print(len(a))
"""
# 620种体积的箱子
# print(f)
# print(len(set(f)))
