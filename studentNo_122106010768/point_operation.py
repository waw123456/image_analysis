#  姓名：王安文
#  学号：122106010768
#  作业名：点运算实验
#  课程：图像分析基础
#  作业实现内容：线性点运算 + 分段线性点运算 + 非线性点运算
import numpy as np
import cv2
import sys


# 线性点运算实现灰度反转  s = 255-r
def linear_point(img):
    height = img.shape[0]
    width = img.shape[1]
    result = np.zeros((height, width), np.uint8)
    for i in range(height):
        for j in range(width):
            gray = -(img[i, j])+255
            result[i, j] = np.uint8(gray)
    return result

# 分段线性点运算实现
# <=80灰度值,灰度扩展，S1 = 2*r+60; >80灰度值，灰度压缩，S2 =  0.2*r
def piece_wise_linear(img):
    height = img.shape[0]
    width = img.shape[1]
    result = np.zeros((height, width), np.uint8)
    for i in range(height):
        for j in range(width):
            if img[i, j] <= 80:
                result[i, j] = 2*img[i, j]+60
            else:
                result[i, j] = 0.2*img[i, j]
    return result

# 非线性点运算实现幂次变换  r=0.5 c=1
def non_linear_point(img):
    result = img ** 0.5
    result = np.uint8(result * 255 / np.max(result))
    return result

if __name__ == "__main__":
    # ------------调用三种点运算函数查看结果---------------#
    img_in = cv2.imread("cat.jpg", 0)
    linear_point_img = linear_point(img_in)
    piece_wise_linear_img = piece_wise_linear(img_in)
    non_linear_point_img = non_linear_point(img_in)

    cv2.namedWindow("线性点运算", 0)
    cv2.namedWindow("分段线性", 0)
    cv2.namedWindow("非线性", 0)

    cv2.resizeWindow("线性点运算", 500, 400)
    cv2.resizeWindow("分段线性", 500, 400)
    cv2.resizeWindow("非线性", 500, 400)

    cv2.imshow("线性点运算", linear_point_img)
    cv2.imshow("分段线性", piece_wise_linear_img)
    cv2.imshow("非线性", non_linear_point_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()












