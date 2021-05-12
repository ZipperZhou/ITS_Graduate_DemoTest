import ImageProcess
import LineProcessing
import trailConfirm
import cv2
import numpy as np


# 取一根中线
def fetch_middle_line(lines, num):
    return lines[num]


# 按顺序将中线上的点的int型坐标拿出来
# 中线上的每个点坐标（转换为int类型），返回两个数组，一个横坐标数组，一个纵坐标数组，横坐标++
# 这个是错误做法：不应该遍历横坐标应该遍历纵坐标，请跳转到right_allY_print_int_site()
def false_allX_print_int_site(floatLine):  # 输入的是floatLine两端点
    # y - y2 = k(x - x2)
    # y = k(x-x2)
    # 拿斜率
    k = LineProcessing.get_slope(floatLine)
    print('k = ', k)
    # 如果不垂直
    if k != 0:
        x_num = int(abs(floatLine[2] - floatLine[0]) + 1)
        x = np.zeros(x_num, dtype=int)
        y = np.zeros(x_num, dtype=int)
        # 选取更小的自变量起点
        starting_point = floatLine[0]
        if floatLine[0] > floatLine[2]:
            starting_point = floatLine[2]
        # x数组重新赋值为 【起点横坐标， 起点横坐标+1， …… ， 终点横坐标】
        for p in range(0, x_num):
            x[p] = int(starting_point + p)
        # print('自变量以此为：', x)
        # 得到中线每个点坐标：
        for q in range(0, x_num):
            y[q] = int(k * (x[q] - floatLine[2]))
            # 打印每个坐标看看
            # print('【', x[q], ' ', y[q], '】')
        return x, y, x_num  # 返回两个一维数组
        # ！！！！这里可以合并两个for，但是为了看数据，先分开
    # 如果垂直，中线坐标点为
    else:
        x = np.zeros(width, dtype=int)
        y = np.zeros(width, dtype=int)
        for q in range(0, width):
            x[q] = floatLine[0]
            y[q] = q
        return x, y, width


# 按顺序将中线上的点的int型坐标拿出来
# 中线上的每个点坐标（转换为int类型），返回两个数组，一个横坐标数组，一个纵坐标数组，横坐标++
# 错误做法：不应该遍历横坐标应该遍历纵坐标
def right_allY_print_int_site(floatLine):  # 输入的是floatLine两端点
    # y - y2 = k(x - x2)        y2 = 0, x2 = floatLine[2]
    # x[g] = y[g]/k +x2
    k = LineProcessing.get_slope(floatLine)
    xArr = np.zeros(width, dtype=int)
    yArr = np.zeros(width, dtype=int)
    for g in range(0, width):
        yArr[g] = g
        xArr[g] = int(g/k + floatLine[2])
        # print(xArr[g], yArr[g])
    return xArr, yArr


# 获取（x, y）的灰度值
def get_gray_value(a, b, img_binary_get):   # 输入的是横纵坐标，输出的却是纵横坐标
    return img_binary_get[b][a]


# 按顺序将灰度值填入一个一维数组
def pick_valueTo_uni_dimension(x_site, y_site):
    array_gray_data = np.zeros(width, dtype=int) 
    print('一维数组size=', width)
    for s in range(0, width):
        array_gray_data[s] = get_gray_value(x_site[s], y_site[s], img2value)
        print(x_site[s], y_site[s], array_gray_data[s])
    # print('灰度值一维数组：', array_gray_data)
    return array_gray_data  # 返回一个一维数组


'''
# 检测连续0长度
extent = detect_continuous_zero(gray_value_gather)  # extent长度
def detect_continuous_zero():
    while 
    return length_ofZero
'''

if __name__ == '__main__':
    img, img2value, complete_middle_lines = trailConfirm.trail_confirm_all()
    cv2.waitKey()
    cv2.destroyAllWindows()
    # 在二值图上绘制中线
    trailConfirm.draw_middleLine(img2value, complete_middle_lines, rough=2)
    '''
    # 二值图输出的实验
    print(img2value[0])
    print('img2value[0] = ', np.size(img2value[0]))
    # 结论：img2value[0] = [600个元素，值只有0 & 255， 其中：0 = 黑 ， 255 = 白 ]，连续黑色为没有车
    '''
    width, height = trailConfirm.get_pic_size(img)
    # 第一种思路
    # 第一次撰写过程中犯了很大的错误，错误在于，求出了每一个x，实际上我们要输出的是每一个y
    # 输出每一个x的话，会在纵向方向上跳过很多个点，导致根本看不到连续白点的存在，样本（数组长度）也不够339个
    # 从图像宽度的2/3处开始检测，因为有车不往前停
    for i in range(0, 3):
        # 取一根中线
        ready_toProcess_midLine = fetch_middle_line(complete_middle_lines, i)
        # 按顺序将中线上的点的int型坐标拿出来
        x_pos, y_pos  = right_allY_print_int_site(ready_toProcess_midLine)
        # 按顺序将灰度值填入一个一维数组
        gray_value_gather = pick_valueTo_uni_dimension(x_pos, y_pos)
    # gray_value_gather : 一维数组{0，255}
    # 检测连续0长度
    '''
    extent = detect_continuous_255(gray_value_gather)  # extent长度
    # 判断连续0的长度是否达到阈值
    judge_ifAttain_threshold(extent)
    # for循环顺序检测一根直线中的255；直到有符合阈值的extent出现，如果没有返回图片高度


    # 第二种思路
    # 先转化像素点代表长度，再转化为检测长度'''
