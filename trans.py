import numpy as np
import ImageProcess
import LineProcessing


def trans_test(original):
    print(original[0][0][0])
    print(original[0][0][1])
    print(original[0][0][2])
    print(original[1][0][0])
    print(original[2][0][0])
    print(original[4][0][3])
    # 第一个数是行数（第n个元组），第二个数是0，第三个数是列数（元组内第n个元素）


# 2021.5.8数组实验
def array_test():
    x1 = [[00, 1], [2, 3]]
    x2 = [[10, 11], [12, 13]]
    x3 = [[20, 21], [22, 23]]
    arr = [x1, x2, x3]
    print(arr)
    print(arr[2][0][0])
    y1 = [[1, 4]]
    y2 = [[2, 5]]
    y3 = [[3, 6]]
    arry = [y1, y2, y3]
    print('\n', arry)
    print(arry[1][0])
    print(arry[1][0][1])



# 定义lines
def line_set():
    l1 = [285, 318, 285, 197]
    l2 = [289, 318, 289, 160]
    l3 = [288, 318, 288, 158]
    l4 = [140, 333, 181, 242]
    l5 = [142, 333, 197, 211]
    l6 = [284, 318, 284, 249]
    l7 = [348,  81,  415, 136]
    l8 = [355, 168, 376, 221]
    l9 = [  7, 338, 66, 266]
    l10 =[10, 338,  71, 262]
    l11 =[352, 163, 373, 216]
    l12 =[286, 318, 286, 170]
    l13 =[ 26, 317,  70, 262]
    line_tuple = [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13]
    return line_tuple

def line_set2():
    l1 = [[285, 318, 285, 197]]
    l2 = [[289, 318, 289, 160]]
    l3 = [[288, 318, 288, 158]]
    l4 = [[140, 333, 181, 242]]
    line_tuple2 = [l1, l2, l3, l4]
    return line_tuple2


def rank(elem):                     # 排序，本来用elem.sort（），但是后来失败了，不知道原因
    return np.sort(elem, axis=0)


def takefirst(arr):
    return arr[0][0]

if __name__ == '__main__':
    lines = line_set()
    print(lines)
    lines.sort()
    lines2 = line_set2()
