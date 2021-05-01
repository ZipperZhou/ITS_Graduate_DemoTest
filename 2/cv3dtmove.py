from time import sleep
import numpy as np
import cv2
import matplotlib.pyplot as plt

kernelX = np.ones((6, 6), np.uint8)
def readav():
    previous_image = None
    #打开视频
    cap = cv2.VideoCapture('1.mp4')

    #detectShadows = True
    fgbg = cv2.createBackgroundSubtractorMOG2(200, 350)

    while (1):
        '''
        参数ret 为True 或者False,代表有没有读取到图片
        第二个参数frame表示截取到一帧的图片
        '''
        ret, frame = cap.read()

        '''
        if(ret):
            print(frame)
            print(len(frame))
            print(len(frame[1]))
            break;
            #print(ret)
        '''
        fgmask = fgbg.apply(frame)
        sleep(0.05)
        fgmask1=cv2.dilate(fgmask, kernelX, iterations = 1)
        fgmask2=cv2.erode(fgmask1, kernelX)
        # 寻找轮廓
        contours, hierarchy = cv2.findContours(fgmask1.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        # 统计选择的检测区域中的轮廓（有效轮廓）
        valid_cntrs = []  # 空列表 valid_cntrs 用于存放有效轮廓
        for cntr in contours:  # 遍历找到的所有轮廓
            x, y, w, h = cv2.boundingRect(cntr)  # 轮廓的坐标
            # 选择的检测区域为 [:200, 80:]
            # 有效轮廓的面积大于等于 25
            if (x <= 200) & (y >= 80) & (cv2.contourArea(cntr) >= 25):
                valid_cntrs.append(cntr)  # 将有效轮廓添加进 valid_cntrs
        cv2.imshow('frame', fgmask2)
        print(valid_cntrs)

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    '''img1 = np.copy(fgmask)
    rows, cols = img1.shape[:2]
    for row in range(rows):
        for col in range(cols):
            if(fgmask[row, col]>10):
                print("hello")
            #fgmask[row, col]反灰度值
    '''
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    #先对视频预处理
    readav()
