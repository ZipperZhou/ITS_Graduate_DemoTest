import numpy as np

length = np.ones(6)


def FirstTime(first_len):
    rest_time = first_len*(-0.4)+80
    print('第一次剩余时间：', rest_time)
    return rest_time


def SecondTime(minus_len, Ftime):
    change_time = minus_len*2.2
    Stime = Ftime - 10
    SecondRestTime = Stime - change_time
    print('第二次调整后剩余时间为', SecondRestTime)
    return SecondRestTime


def AllTimeRG(LengthArray):
    RestTime = 100
    firstLength = LengthArray[1]
    secondLength = LengthArray[4]
    MinusLength = secondLength - firstLength
    rest_time1 = FirstTime(firstLength)
    rest_time = SecondTime(MinusLength, rest_time1)
