#  姓名：王安文
#  学号：122106010768
#  作业名：几何运算实验
#  课程：图像分析基础
#  作业实现内容：实现图像的平移，镜像，旋转 以及符合它们的变换
import numpy as np
import cv2

# 向右平移函数的实现  right>=0
def move(right, img):
    imginfo = img.shape
    result = np.zeros(imginfo, np.uint8)
    for i in range(imginfo[0]):
        for j in range(imginfo[1]-right):
            result[i, j+right] = img[i, j]
    return result

# 垂直镜像函数的实现
def h_acous_tic(img):
    imginfo = img.shape
    result = np.zeros([imginfo[0] * 2, imginfo[1], imginfo[2]], np.uint8)

    for i in range(imginfo[0]):
        for j in range(imginfo[1]):
            result[i, j] = img[i, j]
            result[imginfo[0] * 2 - i - 1, j] = img[i, j]
    return result
# 水平镜像函数的实现
def w_acous_tic(img):
    imginfo = img.shape
    result = np.zeros([imginfo[0], imginfo[1] * 2, imginfo[2]], np.uint8)
    for i in range(imginfo[0]):
        for j in range(imginfo[1]):
            result[i, j] = img[i, j]
            result[i, 2*imginfo[1]-1-j] = img[i, j]
    return result

# 旋转函数的视线
def matrotate(img):
    imginfo = img.shape
    martix = cv2.getRotationMatrix2D((imginfo[0] * 0.5, imginfo[1] * 0.5), 45, 0.7)
    result = cv2.warpAffine(img, martix, (imginfo[0], imginfo[1]))
    return result

# 复合函数 同时平移+旋转+镜像
def all_function(img):
    move1 = move(150, img)
    matrotate1 = matrotate(move1)
    return h_acous_tic(matrotate1)

if __name__ == "__main__":
    img_in = cv2.imread("flower.jpg", 1)
    # 图片向右移动100个像素
    move_img = move(100, img_in)
    # 图片垂直镜像 和水平镜像
    h_acous_tic_img = h_acous_tic(img_in)
    w_acous_tic_img = w_acous_tic(img_in)
    # 图片旋转45度
    matrotate_img = matrotate(img_in)
    # 调用三种变换的符合函数
    last_img = all_function(img_in)

    cv2.namedWindow("向右平移100", 0)
    cv2.namedWindow("垂直镜像", 0)
    cv2.namedWindow("水平镜像", 0)
    cv2.namedWindow("中心旋转45度", 0)
    cv2.namedWindow("复合变换", 0)


    cv2.resizeWindow("向右平移100", 500, 400)
    cv2.resizeWindow("垂直镜像", 500, 400)
    cv2.resizeWindow("水平镜像", 500, 400)
    cv2.resizeWindow("中心旋转45度", 500, 400)
    cv2.resizeWindow("复合变换", 500, 400)


    cv2.imshow("向右平移100", move_img)
    cv2.imshow("垂直镜像", h_acous_tic_img)
    cv2.imshow("水平镜像", w_acous_tic_img)
    cv2.imshow("中心旋转45度", matrotate_img)
    cv2.imshow("复合变换", last_img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print("end")