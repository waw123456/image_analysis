#  姓名：王安文
#  学号：122106010768
#  作业名：基于暗通道先验的图像去雾算法实现
#  课程：图像分析基础
#  作业实现内容：复现dehaze算法
import cv2
import numpy as np
import matplotlib.pyplot as plt

def MinFilterGray(src, r=17):
    # 最小值滤波器
    return cv2.erode(src, np.ones((2*r+1, 2*r+1)))

def guidedfilter(I, p, r, eps):
    height, width = I.shape
    m_I = cv2.boxFilter(I, -1, (r, r))
    m_p = cv2.boxFilter(p, -1, (r, r))
    m_Ip = cv2.boxFilter(I*p, -1, (r, r))
    cov_Ip = m_Ip-m_I*m_p

    m_II = cv2.boxFilter(I*I, -1, (r, r))
    var_I = m_II-m_I*m_I

    a = cov_Ip/(var_I+eps)
    b = m_p-a*m_I

    m_a = cv2.boxFilter(a, -1, (r, r))
    m_b = cv2.boxFilter(b, -1, (r, r))
    return m_a*I+m_b

def getV1(m, r, eps, w, maxV1):   # 输入RGB图  范围[0,1]
    # 计算大气遮罩图像V1和光照值A, V1 = 1-t/A
    # 获取暗道图
    V1 = np.min(m, 2)
    # 使用引导滤波优化
    V1 = guidedfilter(V1, MinFilterGray(V1, 7), r, eps)
    bins = 2000
    ht = np.histogram(V1, bins)
    d = np.cumsum(ht[0])/float(V1.size)
    for lmax in range(bins-1, 0 ,-1):
        if d[lmax]<=0.999:
            break
    A = np.mean(m, 2)[V1>=ht[1][lmax]].max() # 大气光照A
    V1 = np.minimum(V1*w, maxV1)

    return V1,A

def deHaze(m, r=27, eps=0.01, w=0.9, maxV1=0.9, bGamma=False):
    Y = np.zeros(m.shape)
    V1, A = getV1(m, r, eps, w, maxV1)  # 得到遮罩图像和大气光照
    for k in range(3):
        Y[:, :, k] = (m[:, :, k]-V1)/(1-V1/A) # 颜色校正
    Y = np.clip(Y, 0, 1)
    if bGamma:
        Y = Y**(np.log(0.5)/np.log(Y.mean()))
    return Y

if __name__ == "__main__":
    img_in = cv2.imread('fog.jpg')
    # 去雾的效果图
    defog = deHaze(img_in/255.0)*255
    cv2.imwrite('defog.jpg', defog)
    # 去雾效果+Gamma拉伸
    defog_gamma = deHaze(img_in / 255.0, bGamma=True) * 255
    cv2.imwrite('defog_gamma.jpg', defog_gamma)

    defog_img = cv2.imread('defog.jpg')
    defog_gamma_img = cv2.imread('defog_gamma.jpg')

    b, g, r = cv2.split(defog_img)
    defog_img = cv2.merge([r, g, b])

    b, g, r = cv2.split(defog_gamma_img)
    defog_gamma_img = cv2.merge([r, g, b])

    # 汇总显示图片 进行对比
    fig = plt.figure(figsize=(18, 12))
    plt.subplot(221)
    plt.title('Fog', fontsize=15)
    plt.imshow(img_in)

    plt.subplot(222)
    plt.title('defog', fontsize=15)
    plt.imshow(defog_img)

    plt.subplot(223)
    plt.title('defog+gamma', fontsize=15)
    plt.imshow(defog_gamma_img)
    plt.show()
























