import numpy as np
import ImageProcess
from pprint import pprint as pp
import trans


# 得到第a个二维数组(第一个是array【0】)，并且打印这个元组
def takeTuple(array, a):
    print(array[a])
    return array[a]


'''
def take_axis(arr):
    return arr[0]


# 数组排序
def line_rank_me(x, dimension):
    a = np.zeros(13)        # 初始化13条直线
    b = np.zeros(13)        # 初始化13个用于比较的数
    c = np.zeros(13)
    for i in range(0, dimension):
        a[i] = takeTuple(x, i)     # 拿一条直线
        b[i] = take_axis(x)       # 用于排序的数拿出来放在b[i]，这里用第三个数
        c[i] = b[i]
    b.argsort(axis=0)
    # 带着a[一起]
'''


def line_rank_py(test):     # test是二维数组-大师
    pp(test)
    test_after = test[test[:, 0].argsort()]     # 按第一列进行排序
    return test_after


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
        slope = 0.00000000  # 垂直的线令为0
    else:
        slope = float((y2 - y1) / (x2 - x1))    # 因为坐标原点在图片左上角，所以增加一个符号方便理解
    return slope


def print_slope(num, arr):  # num直线个数，arr元组集合
    k = np.zeros(num)
    for t in range(0, num):
        line = takeTuple(arr, t)  # 拿出一条直线,并打印
        k[t] = get_slope(line)  # 求他的斜率
        print('第', t+1, '条直线斜率是：', k[t])


def get_line(lines, x):
    return lines[x]


# 第i条直线 与 x轴 交点的横坐标
def endpoint_x(lines, i):
    line = get_line(lines, i)           # 拿出第i条直线
    k = get_slope(line)
    if k < 0:
        return line[2]+(-(line[3] / k))        # line[2] = x2; line[3] = y2
    if k > 0:
        return line[0]-(line[1] / k)
    if k == 0:
        return line[0]


# 第i条直线 与 y轴 交点的横坐标
def endpoint_y(lines, i):
    line = get_line(lines, i)
    k = get_slope(line)


if __name__ == '__main__':
    prelines = ImageProcess.AllPrepareingProcessing()

    print(prelines)
    count = line_num(prelines)  # 直线数量
    print('start Line process')
    line_raise = line_rank_py(prelines)
    pp(line_raise)
    print(line_raise[0])
    print_slope(count, line_raise)  # 打印直线端点坐标和每一条直线的斜率

