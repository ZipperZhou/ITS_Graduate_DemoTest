import numpy as np
import ImageProcess
import trans


def get_line(prepro):
    return prepro


# 得到第a个二维数组(第一个是array【0】)，并且打印这个元组
def takeTuple(array, a):
    print(array[a])
    return array[a]


# 数组排序
def line_rank(elem_array):
    return np.sort(elem_array, axis=0)


# 得到直线个数（元组）
def line_num(line_tuple):
    return int(np.size(line_tuple) / 4)


# 得到斜率(元组)
def get_slope(Tuple):
    x1 = Tuple[0]
    y1 = Tuple[1]
    x2 = Tuple[2]
    y2 = Tuple[3]
    if (x1 - x2) == 0:
        slope = 99999999
    else:
        slope = float((y1 - y2) / (x1 - x2))
    return slope


def print_slope(num, arr):  #num直线个数，arr元组集合
    k = np.zeros(num)
    for t in range(0, num):
        line = takeTuple(arr, t)  # 拿出一条直线,并打印
        k[t] = get_slope(line)  # 求他的斜率
        print('第', t+1, '条直线斜率是：', k[t])


def line_select_test():
    pass


def line_average():
    pass


if __name__ == '__main__':
    prelines = ImageProcess.AllPrepareingProcessing()
    count = line_num(prelines)  # 直线数量
    print('start Line process')
    line_raise = line_rank(prelines)
    print(line_raise)
    print_slope(count, line_raise)  # 打印直线端点坐标和每一条直线的斜率'''

