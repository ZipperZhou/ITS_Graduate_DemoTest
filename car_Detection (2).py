from time import sleep

import cv2
import numpy as np

kernelX = np.ones((6, 6), np.uint8)

def car_de():
    camera = cv2.VideoCapture ("1.avi")
    camera.open("1.avi")
    car_cascade = cv2.CascadeClassifier('cars.xml')
    while True:
        (grabbed, frame) = camera.read()
        grayvideo = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cars = car_cascade.detectMultiScale(grayvideo, 1.1, 1)
        sleep(0.02)
        for (x,y,w,h) in cars:
         cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
         cv2.imshow("video",frame)
        if cv2.waitKey(1)== ord('q'):
            break
    camera.release()
    cv2.destroyAllWindows()

def readav():
    previous_image = None
    #打开视频
    cap = cv2.VideoCapture('2.avi')

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
        fgmask1=cv2.dilate(fgmask, kernelX)
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
    """
        kernel应该是算子核
        np.ones()返回给定形状和数据类型的新数组，其中元素的值设为1
        这里是np.ones()返回一个23*23的二维数组，元素都为1
        学习opencv3的时候，绘制hsv空间中的2d直方图，必须要将生成的hist数组的格式转换为uint8格式
        否则应用cv2.imshow时图像不能显示！
    """
    kernelX = np.ones((6, 6), np.uint8)
    #car_de()
    readav()
    '''qimg1 = np.copy(fgmask)
        rows, cols = img1.shape[:2]
        for row in range(rows):
            for col in range(cols):
                if(fgmask[row, col]>10):
                    print("hello")
                #fgmask[row, col]反灰度值
        '''

    cv2.destroyAllWindows()
    '''
        # 使用开运算和闭运算让图像边缘成为一个整体
        #kernel = np.ones((11, 11), np.uint8)
        img_edge1 = cv2.morphologyEx(img_edge, cv2.MORPH_CLOSE, kernel)
        cv2.imshow('after_close', img_edge1)
        img_edge2 = cv2.morphologyEx(img_edge1, cv2.MORPH_OPEN, kernel)

        cv2.imshow('after_open', img_edge2)
        # 查找图像边缘整体形成的矩形区域，可能有很多，车牌就在其中一个矩形区域中
        contours, hierarchy = cv2.findContours(img_edge2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            contours轮廓 hierarchy等级
            findContours三个参数：
                第一个参数是寻找轮廓的图像
                第二个参数表示轮廓的检索模式
                    cv2.RETR_TREE 建立一个等级树结构的轮廓
                第三个参数method为轮廓的近似办法
                    cv2.CHAIN_APPROX_SIMPLE 压缩水平方向，垂直方向，对角线方向的元素，
                    只保留该方向的终点坐标，例如一个矩形轮廓只需4个点来保存轮廓信息
            cv2.findContours()函数返回三个值，第二个是轮廓本身，第三个是每条轮廓对应的属性。

        img_pana = cv2.drawContours(img_edge2, contours, -1, (0, 0, 255), 10)
        #contourIdx参数如果是0、1、2、3等，就是绘制contours里面的指定轮廓，如果是-1，就是绘制所有轮廓。
        cv2.imshow('panaroma', img_pana)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return gray_img_, contours
    '''