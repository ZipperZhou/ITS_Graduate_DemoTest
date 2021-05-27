import math

import ImageProcess
import LineProcessing
import trailConfirm
import cv2
import numpy as np


'''
# 二值图输出的实验
print(img2value[0])
print('img2value[0] = ', np.size(img2value[0]))
# 结论：img2value[0] = [600个元素，值只有0 & 255， 其中：0 = 黑 ， 255 = 白 ]，连续黑色为没有车
'''


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
# 正确做法，遍历纵坐标
def right_allY_print_int_site(floatLine):  # 输入的是floatLine两端点
    # y - y2 = k(x - x2)        y2 = 0, x2 = floatLine[2]
    # x[g] = y[g]/k +x2
    k = LineProcessing.get_slope(floatLine)
    xArr = np.zeros(width, dtype=int)
    yArr = np.zeros(width, dtype=int)
    for g in range(0, width):
        yArr[g] = g
        xArr[g] = int(g / k + floatLine[2])
        # print(xArr[g], yArr[g])
    return xArr, yArr


# 获取（x, y）的灰度值
def get_gray_value(a, b, img_binary_get):  # 输入的是横纵坐标，输出的却是纵横坐标
    return img_binary_get[b][a]


# 按顺序将灰度值填入一个一维数组
def pick_valueTo_uni_dimension(x_site, y_site):
    array_gray_data = np.zeros(width, dtype=int)
    print('一维数组size=', width)
    for s in range(0, width):
        array_gray_data[s] = get_gray_value(x_site[s], y_site[s], img2value_copy)
        # print(x_site[s], y_site[s], array_gray_data[s])
    print('灰度值一维数组：', array_gray_data)
    return array_gray_data  # 返回一个一维数组


# 输入正序；获得倒序的！故要调整顺序：
def get_len_equal_criterion_arr(finalPointGather, startCheckingP):      # finalPointGather:正序灰度数组
    # 初始化
    ready_toCheck_point_gather = np.ones(criterion, dtype=int)      # 初始化阈值长度的数组
    for pick in range(0, criterion):        # 填入17个数
        ready_toCheck_point_gather[pick] = finalPointGather[startCheckingP - pick]
        # 图像上看，startCheckingP - pick是起测点往上17个点（含起测点）
    return ready_toCheck_point_gather


# 判断阈值长度内是否连续0
def detect_continuous_zero(arr):  # 输入待检测数组，长度为criterion
    t = True
    for tra in range(0, criterion):  # traverse 遍历
        if arr[tra] == 0:
            pass
        else:
            t = False
            break
    # print('t = ', t)
    return t


# 循环检测每个0
def check_apieceZero(final_array, start_check_point):  # 传入检测灰度值数组和起测点
    size_of_array = np.size(final_array)
    counter = start_check_point
    have_got_trail = False
    while counter in range(criterion, start_check_point + 1):   # 如果前面全满，最后是17个像素点也不太影响，就计算满排队吧
        ready_queue = get_len_equal_criterion_arr(final_array, counter)     # 得到倒序待检测数组ready_queue
        have_got_trail = detect_continuous_zero(ready_queue)        # 是否检测到连续17个0
        counter = counter - 1           # 改变的其实是每次检测的（连续17个数）起测点
        # print('counter = ', counter)
        if have_got_trail:
            break
    if have_got_trail:
        return True, counter+1      # counter+1：起测点的纵坐标
    else:
        return False, 0


# 判断是否为一级拥塞
def if_first_level(count_p):
    had = False
    if count_p > (init_check_point-7):
        had = True
        print('一级拥塞，trail = 0')
    return had


# 计算物理世界实际拥塞长度
def figure_real_trail(length):
    # L=h * tan[arctan(d/h) +α] -d
    # 理论请见：physicsFigureLength 以及 physicsFigureLengthReadMe
    h = 6.2  # 米
    d_min = 20  # 米
    d_max = 220
    d = width - trail
    a = (math.atan(d_max/h))/width      # should be (arctan(d_max/h)) / width
    # a是摄像头安装角度/拍摄到的上下边实际长度
    # 这里估计为180m(d_max), arctan(180/7.5) = 87.6° 垂直分辨率width=339，则
    before_L = math.atan(d_min/h)+a
    print('tan=', math.tan(before_L))
    L = h*(math.tan(before_L)) - d_min
    print('before = ', before_L)
    print('L = ', L)
    return (width - length)*L-d_min


if __name__ == '__main__':
    img, img2value, complete_middle_lines = trailConfirm.trail_confirm_all()
    img2value_copy = img2value.copy()
    cv2.waitKey()
    cv2.destroyAllWindows()
    # 在二值图上绘制中线
    trailConfirm.draw_middleLine(img2value, complete_middle_lines, rough=2)
    width, height = trailConfirm.get_pic_size(img)
    # 起测点：2/3*width
    init_check_point = int((2 / 3) * width)  # 起测点
    criterion = 22  # criterion 标准（阈值）
    trail_arr = np.zeros(3, dtype=int)      # 三列队尾位置数组
    # 第一种思路
    # 第一次撰写过程中犯了很大的错误，错误在于，求出了每一个x，实际上我们要输出的是每一个y
    # 输出每一个x的话，会在纵向方向上跳过很多个点，导致根本看不到连续白点的存在，样本（数组长度）也不够339个
    # 从图像宽度的2/3处开始检测，因为有车不往前停
    for i in range(0, 3):
        # 取一根中线
        ready_toProcess_midLine = fetch_middle_line(complete_middle_lines, i)
        # 按顺序将中线上的点的int型坐标拿出来
        x_pos, y_pos = right_allY_print_int_site(ready_toProcess_midLine)
        # 按顺序将灰度值填入一个一维数组
        gray_value_gather = pick_valueTo_uni_dimension(x_pos, y_pos)
        # gray_value_gather : 一维数组{0，255}
        # 检测连续0长度
        got_it, trail = check_apieceZero(gray_value_gather, init_check_point)
        if got_it:
            print('找到队尾，纵坐标为：', trail)
        else:
            trail = width
            print('没有找到队尾, 完全拥塞，拥塞长度：trail =', trail)
        one_level = if_first_level(trail)
        if one_level:
            trail = 0
        trail_arr[i] = trail
        real_length = figure_real_trail(trail)
        print('real_length=', real_length)
        pic_final = cv2.line(img, (100, trail), (400, trail), (255, 0, 255), 2)
        cv2.imshow('final', pic_final)
        cv2.waitKey()
    # 开始计算实际物理长度

    # 第二种思路,论文撰写
    # 先转化像素点代表长度，再转化为检测长度
