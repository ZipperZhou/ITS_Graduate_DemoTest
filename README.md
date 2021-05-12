# ITS_Graduate_DemoTest
test for clone ,upload, and design
项目概述：
取一张静态图片，检测车道，相邻车道取中线，检测中线上的灰度值（二值图），确定车队队尾，根据长度设计红绿灯配时。

工程文件：
四个.py文件：
	ImageProcess 图像预处理
	LineProcessing：确定车道线方程
	trailConfirm：确定中线方程并绘制
	check：检测中线上的像素点灰度值（二值图）

声明：
	在check.py中
	变量声明：
	img原图，img2value二值图;
	complete_middle_lines中线集合
		（一共三条中线，运行工程可看到被绘制的三条中线）中线描述格式：两端点坐标式（x1, y1, x2, y2）
	（x_pos[s]，y_pos[s])中线上第i个点的坐标（坐标原点为图片左上角，向右为x轴正方向，向下为y轴正方向）
	图像大小width=339, length = 600

函数声明:
	取一条中线:	 fetch_middle_line(lines, num):
	按顺序将中线上的点的int型坐标拿出来:    right_allY_print_int_site(floatLine)，
					输入为一根中线,return 横坐标数组， 纵坐标数组（按顺序的，是对应的）
	按顺序将中线上每一个点的灰度值填入一个一维数组:	pick_valueTo_uni_dimension(x_site, y_site):
	获取（x, y）的灰度值 # 输入的是横纵坐标，输出的却是纵横坐标:	get_gray_value(a, b, img_binary_get): 
	
问题：输出的像素值数组为全0，（灰度0表示黑，灰度255表示白），可是从运行图（drawOn2value.jpg）可明显观察到，中线是经过了很多白色的点的。大师救我！
