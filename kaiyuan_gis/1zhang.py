# -*- coding: utf-8 -*-
# @Time    : 2020/7/6 13:31
# @Author  : ding
# @File    : 1zhang.py

import os
from osgeo import ogr, gdal, osr
from osgeo import gdalconst
import shapely
import numpy as np

# gdal.AllRegister()  一次性注册所有驱动，只能读不能写。
driver_gdal = gdal.GetDriverByName('Gtiff')
driver_gdal.Register()
driver_all = gdal.GetDriverCount()
print(driver_all)

changsha_tif = gdal.Open(r'E:\gistest\data\430000HN\430000HN_L5_TM_1990\430000HN_L5_TM_1990_R1C1.TIF')

print(dir(changsha_tif))  # 查看可操作
print(changsha_tif.GetDescription())  # 返回路径信息
print(changsha_tif.RasterCount)  # 数据集上的波段数，每一个波段都是一个数据集。
print(changsha_tif.RasterXSize)
print(changsha_tif.RasterYSize)  # y方向上的像元个数
print(changsha_tif.GetProjection())  # 投影
print(changsha_tif.GetGeoTransform())  # 六参数

# 读取栅格数据的元数据
print(changsha_tif.GetMetadata())
# 获取波段信息，波段操作
changsha_band = changsha_tif.GetRasterBand(1)  # 获取栅格数据的第一个波段信息,索引从1开始。
print(dir(changsha_band))
print(changsha_band.DataType)
print(changsha_band.XSize)
print(changsha_band.YSize)  # 获取宽和高
print(changsha_band.GetNoDataValue())  # 无意义值
print(changsha_band.ComputeRasterMinMax())  # 最大最小值
# print(changsha_band.GetNoDataValue())


# 访问栅格数据中的像元
print(dir(gdalconst))  # GDT开头的就是数据类型
# 1:'GDT_Byte', 'GDT_CFloat32', 'GDT_CFloat64',
# 'GDT_CInt16', 'GDT_CInt32', 'GDT_Float32',
# 7:'GDT_Float64', 'GDT_Int16', 5:'GDT_Int32',
# 'GDT_TypeCount', 'GDT_UInt16', 'GDT_UInt32', 0:'GDT_Unknown'
print(changsha_band.DataType)  # 输出数字对应上文的数值类型 1对应'GDT_Byte',与numpy相对应。

# 访问数据集的数据 ReadRaster()二进制   ReadAsArray()以数组形式
# 读取数据，再对数据进行计算分析,参数定义 P57
print(changsha_band.ReadAsArray(0, 0, 3, 3))  # 波段数据
print(changsha_tif.ReadAsArray(0, 0, 3, 3))  # 栅格数据 有7个波段，打印出7个数组，缩放就是重采样

# 创建与保存栅格数据集
driver_tif = gdal.GetDriverByName('GTiff')
print(driver_tif.GetMetadata())  # 查看是否支持create or createcopy
if 'DCAP_CREATE' in driver_tif.GetMetadata() and driver_tif.GetMetadata()['DCAP_CREATE'] == 'YES':
    src_file = r'E:\gistest\data\430100changsha\430100CSX_L5_TM_1990\430100CSX_L5_TM_1990_R1C1.tif'
    dst_file = r'E:\gistest\data\430100changsha\430100CSX_L5_TM_1990\copy_test.tif'
    src_ds = gdal.Open(src_file)
    dst_ds = driver_tif.CreateCopy(dst_file, src_ds, 0)

create_tif = driver_tif.Create(r'E:\gistest\data\430100changsha\430100CSX_L5_TM_1990\create_test.tif',
                         512, 512, 1, gdal.GDT_Byte)
create_tif.SetGeoTransform([-271440.0, 90.0, 0.0, 3451680.0, 0.0, -90.0])
srs = osr.SpatialReference()
srs.SetUTM(11, 1)
srs.SetWellKnownGeogCS('NAD27')
create_tif.SetProjection(srs.ExportToWkt())
create_tif.GetRasterBand(1).WriteArray(np.zeros((512, 512)))



# extfile = r'E:\gistest\kaiyuan_gis\point_test.shp'
#
# driver = ogr.GetDriverByName("ESRI Shapefile")
# if os.access(extfile, os.F_OK):
#     driver.DeleteDataSource(extfile)
# newds = driver.CreateDataSource(extfile)  # 创建shp文件
# layernew = newds.CreateLayer('point', None, ogr.wkbPoint)  # 创建点要素
