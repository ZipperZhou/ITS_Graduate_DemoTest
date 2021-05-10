import cv2
import numpy as np
import LineProcessing


def set_lane():
    lines = [[10, 338,  71, 262],
             [26, 317,  70, 262],
             [142, 333, 197, 211],
             [286, 318, 286, 170],
             [355, 168, 376, 221]]
    return lines


def get_lane(lanes, num):
    return lanes[num]


def get_middle_line(lane1, lane2):
    x1 = (lane1[0] + lane2[0])/2
    y1 = (lane1[1] + lane2[1])/2
    x2 = (lane1[2] + lane2[2])/2
    y2 = (lane1[3] + lane2[3])/2
    middle_line = [x1, y1, x2, y2]
    return middle_line


def figure_equation(lane):
    x1 = lane[0]
    y1 = lane[1]
    x2 = lane[2]
    y2 = lane[3]
    LineProcessing.get_slope(lane)
    # y = kx - kx1 +y1
    return



if __name__ == '__main__':
    done_line = set_lane()        # 确定车道线合集
    print(done_line)
    # 拿两条相邻车道线
    middle_line_gather = np.zeros((3, 4))   # 最右侧车道不进行计算，因为是BRT车道
    for i in range(0, 3):
        z1 = get_lane(done_line, i)
        z2 = get_lane(done_line, i+1)
        # 求两线的中线
        middle_line_gather[i] = get_middle_line(z1, z2)
    print('三条中线：')
    print(middle_line_gather)












