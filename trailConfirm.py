import cv2
import numpy as np
import ImageProcess
import LineProcessing


def set_lane():
    lines = [[9, 338, 74, 261],
             [145, 333, 200, 211],
             [302, 318, 302, 157],
             [352, 163, 373, 216]]
    return lines


def get_lane(lanes, num):
    return lanes[num]


# false middle line process
def get_middle_line_gather(lane1, lane2):
    x1 = (lane1[0] + lane2[0])/2
    y1 = (lane1[1] + lane2[1])/2
    x2 = (lane1[2] + lane2[2])/2
    y2 = (lane1[3] + lane2[3])/2
    middle_line = [x1, y1, x2, y2]
    return middle_line


def fake_middle_line(done_line_copy):
    middle_line_gather = np.zeros((3, 4))  # 最右侧车道不进行计算，因为是BRT车道
    for i in range(0, 3):
        z1 = get_lane(done_line_copy, i)
        z2 = get_lane(done_line_copy, i + 1)
        # 求两线的中线
        middle_line_gather[i] = get_middle_line_gather(z1, z2)
    print('fake三条中线：')
    print(middle_line_gather)
    return middle_line_gather


# true figure out middle lines
def get_pic_size(img_colorful):
    width, length = ImageProcess.check_size(img_colorful)     # size= (339, 600, 3)
    return width, length


def complete_lane_width339(lane):      # y=339时，x的坐标
    # y-339 = k(x-x0)  -> y1 - 339 = k(x1 - x0)
    # x0 = x1 +(339-y1)/k
    # gen是y = 339（底线处）时x的坐标，得到这个坐标，可以更新lane的第一组坐标
    k = LineProcessing.get_slope(lane)
    if k != 0:
        gen = lane[0] + (338 - lane[1])/k
    else:
        gen = lane[0]
    return gen


def complete_lane_width0(lane):
    # y-0 = k(x-x0)  ->   y2 - 0 = k(x2 - x0)
    # x0 = x2 - y2/k
    # ji是y = 0（远处，屏幕上顶）时x的坐标，得到这个坐标，可以更新lane的第二组坐标
    k = LineProcessing.get_slope(lane)
    if k != 0:
        ji = lane[2] - (lane[3]/k)
    else:
        ji = lane[0]
    return ji


def update_lane_to339(lines):
    for co in range(0, 4):
        new_x1 = complete_lane_width339(lines[co])     # get新横坐标
        lines[co][0] = new_x1
        lines[co][1] = 338
    return lines


def update_lane_to0(lines):
    for bo in range(0, 4):
        new_x2 = complete_lane_width0(lines[bo])
        lines[bo][2] = new_x2
        lines[bo][3] = 0
    return lines


def figure_middle_line_true(lane1, lane2):
    middle_point_floor = (lane1[0] + lane2[0])/2       # lane[1] = 339
    middle_point_top = (lane1[2] + lane2[2])/2
    middle_line_tuple = [middle_point_floor, 339, middle_point_top, 0]
    return middle_line_tuple


def get_middle_line(middle_gather, num):
    if num < 3:
        return middle_gather[num]
    else:
        print('没那么多中线')


def aggregate_middle_line(lines):
    middle_line_gather_true = np.zeros((3, 4))
    for n in range(0, 3):
        # true 计算中线方程（两点式）
        middle_line = figure_middle_line_true(lines[n], lines[n+1])
        middle_line_gather_true[n] = middle_line
    return middle_line_gather_true


'''
def figure_equation(lane):
    x1 = lane[0]
    y1 = lane[1]
    x2 = lane[2]
    y2 = lane[3]
    LineProcessing.get_slope(lane)
    # y = kx - kx1 +y1
    return
'''


# 绘制中线
def fl_trans_int(data):     # float转为int，绘制时的坐标需要int
    return int(data)


def draw_middleLine(img, draw_line, rough):
    for j in range(0, 3):
        m_line = get_middle_line(draw_line, j)
        x1 = fl_trans_int(m_line[0])
        y1 = fl_trans_int(m_line[1])
        x2 = fl_trans_int(m_line[2])
        y2 = fl_trans_int(m_line[3])
        print('绘制的中线两端坐标【', x1, ' ', y1, ' ', x2, ' ', y2, '】')
        pic_with_mid = cv2.line(img, (x1, y1), (x2, y2), (0, 255, 255), rough)
        cv2.imshow('middle', pic_with_mid)
        cv2.waitKey()


'''
if __name__ == '__main__':
'''


def trail_confirm_all():
    done_line = set_lane()        # 确定车道线合集
    done_line_copy = done_line.copy()
    print('车道线：', done_line)
    # 拿两条相邻车道线
    fake_middle_line_gathers = fake_middle_line(done_line_copy)
    print('看着！我要更新了线段了！！！！！')
    updated_done_line_half = update_lane_to339(done_line)
    updated_done_line = update_lane_to0(updated_done_line_half)
    print('更新后的完整车道线两点式方程：', updated_done_line)
    true_middle_lines = aggregate_middle_line(updated_done_line)
    # 绘制中线
    print('start drawing primary img')
    img_color, img_binary = ImageProcess.pp2value()
    img_binary2 = img_binary.copy()
    # draw_middleLine(img_color, fake_middle_line_gathers, 3)
    draw_middleLine(img_color, true_middle_lines, 3)
    return img_color, img_binary, true_middle_lines














