import cv2
import numpy as np
import trans
import LineProcessing


# 读取图片、调整尺寸、灰度化
def readphoto(img_path):
    Photo0 = cv2.imread(img_path, flags=cv2.IMREAD_COLOR)

    return Photo0


def resize_photo(imgArr, MAX_WIDTH=600):
    img = imgArr
    rows, cols = img.shape[:2]  # 获取图像宽和高
    if cols > MAX_WIDTH:
        change_rate = MAX_WIDTH / cols
        img = cv2.resize(img, (MAX_WIDTH, int(rows * change_rate)), interpolation=cv2.INTER_AREA)
    return img


def check_size(Photo):
    sp = Photo.shape
    print("size=", sp)  # 查看图片大小
    sz1 = sp[0]  # width(rows) of image
    sz2 = sp[1]  # heights(colums) of image
    sz3 = sp[2]  # the pixels value is made up of three primary colors
    print('width: %d \nheight: %d \nnumber: %d' % (sz1, sz2, sz3))
    return sz1, sz2


def process(Photo):
    # 复制出一个直线检测图
    # 灰度变化
    Photo_gray = cv2.cvtColor(Photo, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Photo_gray', Photo_gray)
    cv2.waitKey()
    # 高斯滤波
    blur = cv2.GaussianBlur(Photo_gray, (5, 5), 0)
    # 二值化
    ret, binary = cv2.threshold(blur, 130, 255, cv2.THRESH_BINARY)
    cv2.imshow('2value', binary)
    cv2.waitKey()
    '''OTSU二值化
    _, binary2 = cv2.threshold(Photo_gray, 0, 255, cv2.THRESH_OTSU)
    cv2.imshow('2value', binary2)
    cv2.waitKey()
    '''
    # canny
    Photo_canny = cv2.Canny(binary, 350, 200, 3)
    cv2.imshow('canny', Photo_canny)
    cv2.waitKey()

    # 试着做膨胀腐蚀处理
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 2))
    kernelBig = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 5))
    kernelX = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 4))
    kernelY = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 3))

    erode_dilate = cv2.dilate(binary, kernel)
    cv2.imshow('dilate', erode_dilate)
    erode_dilate = cv2.erode(erode_dilate, kernel)
    cv2.imshow('erode', erode_dilate)
    '''
    erode_dilate = cv2.dilate(erode_dilate, kernelY)
    cv2.imshow('dilate', erode_dilate)
    erode_dilate = cv2.erode(erode_dilate, kernelY)
    cv2.imshow('erode', erode_dilate)
    cv2.waitKey()
    '''

    # sobel
    x = cv2.Sobel(blur, cv2.CV_16S, 1, 0)
    y = cv2.Sobel(blur, cv2.CV_16S, 0, 1)
    absX = cv2.convertScaleAbs(x)  # 转回unit8
    absY = cv2.convertScaleAbs(y)
    dst_sobel = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)
    cv2.imshow('absX', absX)
    cv2.imshow('absY', absY)
    cv2.imshow('soble', dst_sobel)
    cv2.waitKey()

    return binary, erode_dilate, Photo_canny, dst_sobel


def HoughChange(Photo, edge_canny, edge_sobel, erode_dilate):  # edge means 边缘
    # 进阶的Hough检测
    lines_C = cv2.HoughLinesP(erode_dilate, rho=2, theta=3 * np.pi / 180, threshold=50, minLineLength=50, maxLineGap=5)
    for i in range(len(lines_C)):  # range计数，len长度
        x_1, y_1, x_2, y_2 = lines_C[i][0]
        cv2.line(Photo, (x_1, y_1), (x_2, y_2), (0, 255, 0), 1)
        # line绘制直线（原图，起点，终点，颜色，宽度）
    print("code successful!")
    print(lines_C)

    cv2.imshow("Hough_line_Canny", Photo)
    cv2.waitKey(0)
    '''
    lines： 输出直线，里面的元素是Vec4i类型，存放直线的坐标信息。
    rho：极坐标ρ的划分步长。
    theta：极坐标θ的划分步长。
    threshold：累加器阈值，达到该阈值认为是一条直线。
    minLineLength：最小线段长度，达到该长度才认为是一条直线。
    maxLineGap： 最大线段间隔，两条共线的线段距离小于该值时认为是一个直线
    '''
    # hough
    '''
    lines = cv2.HoughLines(erode_dilate, rho=1, theta=1 * np.pi / 180, threshold=30, srn=0, stn=0, min_theta=0, max_theta=0.05)
    for i in range(0, len(lines)):
        rho, theta = lines[i][0][0], lines[i][0][1]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(Photo, (x1, y1), (x2, y2), (0, 0, 255), 2)
    cv2.imshow("Hough_line", Photo)
    '''
    return lines_C


def origin_line_count_get(elem):
    number = np.size(elem) / 4
    print('一共有', int(number), '条直线')
    return int(number)


# hough的结果赋给新数组，ori原生数组，prepro待处理的新数组
# 第一个数是行数（第n个元组），第二个数是0，第三个数是列数（元组内第n个元素）
def originlines_Trans_Preprolines(dimension, ori):  # dimension维
    prepro = np.zeros((dimension, 4))
    for i in range(0, dimension):
        for j in range(0, 4):
            # print(ori[i][0][j], '   ', t)
            prepro[i][j] = ori[i][0][j]
    return prepro


# 废弃
def threeToTwo(ori, prepro):
    for twoNum in ori:
        for oneNum in twoNum:
            prepro.append(oneNum)
    return prepro


# 为了确定参考系，画条线看看
def site_confirm(Photo):
    cv2.line(Photo, (3, 3), (100, 150), (0, 255, 255), 4)
    cv2.imshow('site_confirm_test', Photo)
    cv2.waitKey()


def pp2value():
    path = r'D:/graduate/test/13.jpg'
    img0 = readphoto(path)
    img_resize = resize_photo(img0)  # img1是调节尺寸后的图片
    check_size(img_resize)
    cv2.imshow('resize', img_resize)
    cv2.waitKey()
    # process函数：input：原图；  return binary（二值图）, erode_dilate（一次e&r图）, Photo_Canny, dst_sobel（sobel图）
    img_bin, imgErodeDilate, imgCanny, imgSobel = process(img_resize)
    return img_resize, img_bin


def AllPrepareingProcessing():
    path = r'D:/graduate/test/13.jpg'
    img0 = readphoto(path)
    img_resize = resize_photo(img0)  # img1是调节尺寸后的图片
    width, length = check_size(img_resize)
    cv2.imshow('resize', img_resize)
    cv2.waitKey()
    # process函数：input：原图；  return binary（二值图）, erode_dilate（一次e&r图）, Photo_Canny, dst_sobel（sobel图）
    img_bin, imgErodeDilate, imgCanny, imgSobel = process(img_resize)
    # hough函数: input: 原图，canny图，sobel图， 一次e&r图
    origin_lines = HoughChange(img_resize, imgCanny, imgSobel, imgErodeDilate)
    size = origin_line_count_get(origin_lines)

    # trans.trans_test(origin_lines)  # 提取hough结果赋值新数组，二维数组：num*4
    ready_pro_line = originlines_Trans_Preprolines(size, origin_lines)

    # try:三维-二维，二维-二维
    # ready_pro_line = threeToTwo(origin_lines, conduct_lines)
    print(ready_pro_line)
    site_confirm(img_resize)
    return ready_pro_line


# if __name__ == '__main__':
