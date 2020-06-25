# -*- coding: utf-8 -*-
# @Time    : 2020/6/21 15:26
# @Author  : ding
# @File    : gisTest.py

from osgeo import gdal  # 栅格数据
from osgeo import osr   # 矢量数据
import numpy as np
import cv2
import matplotlib.pyplot as plt

np.set_printoptions(threshold=np.inf)  # 使print大量数据不用符号...代替而显示所有

dataset = gdal.Open(r"F:\jupyter\gis\data\430000HN\430000HN_L5_TM_1990\430000HN_L5_TM_1990_R1C1.TIF")

print(dataset.GetDescription())  # 数据描述

print(dataset.RasterCount)  # 波段数

cols = dataset.RasterXSize  # 图像长度
rows = (dataset.RasterYSize)  # 图像宽度

xoffset = cols / 2
yoffset = rows / 2

band = dataset.GetRasterBand(3)  # 取第三波段
r = band.ReadAsArray(xoffset, yoffset, 1000, 1000)  # 从数据的中心位置位置开始，取1000行1000列数据

band = dataset.GetRasterBand(2)
g = band.ReadAsArray(xoffset, yoffset, 1000, 1000)

band = dataset.GetRasterBand(1)
b = band.ReadAsArray(xoffset, yoffset, 1000, 1000)


img2 = cv2.merge([r, g, b])
plt.imshow(img2)
plt.xticks([]), plt.yticks([])  # 不显示坐标轴
plt.show()
