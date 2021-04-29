import os
import re
import cv2
import numpy as np
import matplotlib.pyplot as plt

# 得到 frames 文件夹中所有图像的文件名
col_frames = os.listdir('frames/')

# 根据文件名给所有图像排序
col_frames.sort(key=lambda f: int(re.sub('\D', '', f)))

# 空列表 col_images 用于存放加载进来的图像
col_images = []

for i in col_frames:
    # 加载图像
    img = cv2.imread('frames/' + i)
    # 将图像加载到 col_images 中
    col_images.append(img)

# 视频路径
pathOut = 'vehicle_detection_v3.mp4'

# 帧率（每秒多少帧）
fps = 14.0

# 每帧的图像尺寸
size = (col_images[0].shape[1], col_images[0].shape[0])

# 写入视频
out = cv2.VideoWriter(pathOut, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

# 用于图像膨胀的核
kernel = np.ones((4, 4), np.uint8)

# 字体类型
font = cv2.FONT_HERSHEY_SIMPLEX

for i in range(len(col_images) - 1):

    # 帧差分技术检测车辆目标
    grayA = cv2.cvtColor(col_images[i], cv2.COLOR_BGR2GRAY)  # 上一帧图像
    grayB = cv2.cvtColor(col_images[i + 1], cv2.COLOR_BGR2GRAY)  # 下一帧图像
    diff_image = cv2.absdiff(grayB, grayA)  # 两帧图像之差

    # 图像阈值化
    ret, thresh = cv2.threshold(diff_image, 30, 255, cv2.THRESH_BINARY)

    # 图像膨胀
    dilated = cv2.dilate(thresh, kernel, iterations=1)

    # 寻找轮廓
    contours, hierarchy = cv2.findContours(dilated.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # 统计选择的检测区域中的轮廓（有效轮廓）
    valid_cntrs = []  # 空列表 valid_cntrs 用于存放有效轮廓
    for cntr in contours:  # 遍历找到的所有轮廓
        x, y, w, h = cv2.boundingRect(cntr)  # 轮廓的坐标
        # 选择的检测区域为 [:200, 80:]
        # 有效轮廓的面积大于等于 25
        if (x <= 200) & (y >= 80) & (cv2.contourArea(cntr) >= 25):
            valid_cntrs.append(cntr)  # 将有效轮廓添加进 valid_cntrs

    # 把每一帧中找到的有效轮廓添加到原始帧上
    dmy = col_images[i].copy()
    cv2.drawContours(dmy, valid_cntrs, -1, (127, 200, 0), 2)

    cv2.putText(dmy, "vehicles detected: " + str(len(valid_cntrs)), (55, 15), font, 0.6, (0, 180, 0), 2)
    cv2.line(dmy, (0, 80), (256, 80), (100, 255, 255))
    out.write(dmy)

out.release()