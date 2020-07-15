# -*- coding: utf-8 -*-
# @Time    : 2020/7/7 15:23
# @Author  : ding
# @File    : 4zhang.py

from pprint import pprint
import os
from pyproj import P roj  # 主要进行经纬度与坐标之间的转换
from pyproj import transform  # 在相同基准面下的两个不同投影的变换  cs2cs
from pyproj import Geod  # 计算地球大圆两点间的距离和相对方位，插入等分点等
from osgeo import osr  # 处理空间参考信息  创建投影
from osgeo import gdal  # 处理栅格数据
from osgeo import gdalconst  # 绑定了gdal中的一些常量
from osgeo import ogr  # 处理矢量数据
import fiona  # 读写 处理矢量数据
from PIL import Image  # 栅格数据读写 基于像元
import cv2
import tifffile
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap  # 地图制作
import mpl_toolkits.basemap

import shapely
import sqlite3

import numpy as np
import shapefile  # pyshp
import geojson
import folium

import geopandas as gpd

# ***************************************************************
# 数据测试
for cur_dir, dirs, files in os.walk(r'E:\gistest\b26573ab\中国主要水系-shp'):
    for f in files:  # 当前目录下的所有文件
        # if f.endswith('.shp'):
        if f == 'Taihu.shp':
            file_path = os.path.join(r'E:\gistest\b26573ab\中国主要水系-shp', f)
            gdf = gpd.read_file(file_path)
            pprint(gdf.head(5))
            gdf.plot()


# plt.show()
# ***************************************************************

def scale_percentile(matrix):
    w, h, d = matrix.shape
    matrix = np.reshape(matrix, [w * h, d]).astype(np.float64)
    # Get 2nd and 98th percentile
    mins = np.percentile(matrix, 1, axis=0)  # 1% 分位数
    maxs = np.percentile(matrix, 99, axis=0) - mins
    matrix = (matrix - mins[None, :]) / maxs[None, :]
    matrix = np.reshape(matrix, [w, h, d])
    matrix = matrix.clip(0, 1)
    return matrix


guojie_polygon = r'E:\gistest\data\400guojiaSHP\国界_polygon.shp'
# ogr操作矢量图
# create shapefile
create_path = r'E:\gistest\testdata\create_shapeFile.shp'
driver = ogr.GetDriverByName('ESRI Shapefile')
if os.access(create_path, os.F_OK):
    driver.DeleteDataSource(create_path)
new_source = driver.CreateDataSource(create_path)
newlayer = new_source.CreateLayer('point', None, ogr.wkbPoint)
# 创建属性字段
field_name = ogr.FieldDefn('ID', ogr.OFTInteger)  # field属性字段
newlayer.CreateField(field_name)
# 创建几何要素
point_list = [[100, 200], [50, 10], [19, 20]]
for index, i in enumerate(point_list):
    geom = ogr.CreateGeometryFromWkt('POINT({0} {1})'.format(i[0], i[1]))
    feat = ogr.Feature(newlayer.GetLayerDefn())
    feat.SetField('ID', index)
    feat.SetGeometry(geom)
    newlayer.CreateFeature(feat)
new_source.Destroy()  # 提交并释放资源

# 可视化
gdf = gpd.read_file(create_path)
gdf.plot()
print(gdf)

# 地图投影：建立地球表面上的点与投影平面上点的一一对应关系
# 地球上点一般为经纬度表示，投影平面一般为直角坐标
# 选定一个一定大小的椭球体,并确定它与大地水准面的相关位置
# 大地水准面是指与平均海水面重合并延伸到大陆内部的水准面。是正高的基准面。
# 地球椭球体：大地水准面包围的‘大地球体’，可用数学几何表达。长、短轴，扁率等。
# 基准面：将椭球体定位后，所确定的具有明确方向的椭球体，即基准面，它定义了经线和纬线的原点及方向。
# 地理投影类型包括:等角 等面积 等距
# 常用地理投影:高斯-克吕格  墨卡托(方向角度正确)   UTM（横轴墨卡托）

# 表达坐标系的方式有好几种，有OpenGIS的WKT知名文本;有Proj4的表达方式;有EPSG权威编码方式等
# WKT包含内容如下：# 1、一个总体的坐标系名 # 2、一个地理图形坐标系统名# 3、一个基准面定义
# 4、一个椭球体的名字。长半轴(semi-major axis)和反扁率(inverse flattening)
# 5、本初子午线(prime meridian)名和其与格林威治子午线的偏移值# 6、投影方法类型（如横轴莫卡托）
# 7、投影参数列表（如中央经线等）# 8、一个单位的名称和其到米和弧度单位的转换参数
# 9、轴线的名称和顺序# 10、在预定义的权威坐标系中的编码（如EPSG）

# 水准面=>椭球体=>基准面
# 预定义坐标系统:EPSG

# 投影问题：空间参考与坐标转换 PROJ.4  osr
# PROJ.4:主要是经纬度与地理坐标转换、坐标系转换、基准变换。
# osr更加关注数据层面的投影与投影变换。
# 地图投影表示方法：WGS84空间坐标系统 NAD27等  EPSG编码（投影或者地理坐标）  proj4字符串定义 WKT文本定义
utm = Proj('+proj=utm +zone=10 +ellps=krass')  # 学习一下定义投影的关键字。
china_area_proj = Proj('+proj=aea +lon_0=105 +lat_1=25 +lat_2=47 +ellps=krass')  # 学习一下定义投影的关键字。
x, y = utm(100, 30)
print(x, y)
# 投影变换
x1, y1 = transform(china_area_proj, utm, 0.1, 3847866)
print(x1, y1)
china_area_geod = Geod('+proj=aea +lon_0=105 +lat_1=25 +lat_2=47 +ellps=krass')

# 坐标系统：地理坐标（经纬度）  投影坐标（utm 单位为米）
osrs = osr.SpatialReference()  # 描述地理坐标
osrs.SetWellKnownGeogCS("WGS84")  # 设置标准的坐标系统
osrs_wkt = osrs.ExportToWkt()
print(osrs_wkt)
# osrs.SetWellKnownGeogCS("EPGS:4326")    # 设置标准的坐标系统
# 定义投影系统  高斯-克吕格  墨卡托(方向角度正确)   UTM（横轴墨卡托）
# 是基于地理坐标系统进行定义的
osrs1 = osr.SpatialReference()
osrs1.SetProjCS('UTM 17 (WGS84)')
osrs1.SetWellKnownGeogCS('WGS84')
osrs1.SetUTM(17, True)
osrs_wkt1 = osrs1.ExportToPrettyWkt()  # 字段了解一下
print(osrs_wkt1)
# 可从栅格文件与矢量文件获取投影信息  判断投影信息是否相同 IsSame()

# 不同坐标系桶之间的转换
# osr.CoordinateTransformation


# 文件格式
# 栅格数据的文件格式 geotiff  png jepg
# 栅格数据的（像元或行列坐标）坐标信息表示方式：1.仿射地理变换 2.地面控制点
# 仿射地理变换包括六个参数，栅格数据只存储左上角像元坐标，其他依靠像元大小，xy方向在原点的偏移计算。
# 地面控制点GCP：一个数据集将会有一套控制点关联栅格位置和地理参考系统的一个或者多个位置。所有的控制点共享一个地理参考坐标系统。
# GCP即将栅格数据点与实际地面坐标的点联系起来的。
# 配准，可以将一张没有空间信息的栅格图片变成有地理信息的图，只要在一个已知的坐标系统中定位几个控制点，然后输入这几个点对应的地理位置，就建立了对应关系。
# 栅格波段：类似于图片的rgb通道，
hunan_tif = r'E:\gistest\data\430000HN\430000HN_L5_TM_1990\430000HN_L5_TM_1990_R1C1.TIF'
# 获取驱动
driver_tif = gdal.GetDriverByName("GeoTiff")
# print(gdal.GetDriver(1).LongName)
# 栅格数据集：由栅格的波段数据以及所有波段都有的共同属性构成。
hunan_tif = gdal.Open(hunan_tif)
print(hunan_tif.RasterCount)  # 波段数
print(hunan_tif.GetDescription())  # 描述信息
print(hunan_tif.RasterXSize)  # x方向像元个数 相应的还有y， 可获得栅格数据的大小
print(hunan_tif.GetGeoTransform())  # 栅格数据六参数
print(hunan_tif.GetProjection())  # 栅格 投影
print(hunan_tif.GetGCPs())
# print(hunan_tif.GetGeoTransform())
# 读取元数据 元数据（Metadata），又称中介数据、中继数据，为描述数据的数据（data about data），主要是描述数据属性（property）的信息
print(hunan_tif.GetMetadata())
band1 = hunan_tif.GetRasterBand(1)
print(band1.XSize)
print(band1.DataType)  # 返回实际数值的数据类型
print(band1.ComputeRasterMinMax())
# 访问栅格数据的像元 gdalconst
# 访问数据集数据 即像元灰度值
temp_tif = band1.ReadAsArray(0, 0, 10, 10)
print(temp_tif)

# 创建栅格数据集   除了数据本身，还有投影 元数据信息等
# 1.查看gdal驱动是否支持创建格式
# im = Image.open(r'E:\gistest\data\430100changsha\430100CSX_L5_TM_1990\430100CSX_L5_TM_1990_R1C2.tif').convert('L')
# im.show()
img = tifffile.imread(r'E:\gistest\data\430100changsha\430100CSX_L5_TM_1990\430100CSX_L5_TM_1990_R1C1.tif')
# cv2.namedWindow("Image")
# cv2.imshow("Image", img)
# cv2.waitKey(100)
# cv2.destroyAllWindows()
print(img.shape)
# p1 = plt.subplot()
# p1.imshow(scale_percentile(img[:, :, :4]))


# 矢量数据的文件格式有:GeoJson（字典）、WKT WKB（文本、字符串）、shapefile、spatiaLite、TAB
# 要素feature， 一个图层包含一层要素与要素定义。要素里包含空间数据与属性
driver_shp = ogr.GetDriverByName("ESRI Shapefile")
guojiePolygon = driver_shp.Open(guojie_polygon, update=1)
# 图层的概念，有同种要素组成在一起的层。  要素类：相同几何形状的要素集合。  要素数据集：具有相同坐标系统的要素类的集合。
layer1 = guojiePolygon.GetLayer(0)
print(layer1.GetFeatureCount())  # 要素个数  要素：点线面即为要素的抽象模型
print(layer1.GetExtent())  # 图层空间范围  东南西北四至
# 图层属性dbf
layerdef = layer1.GetLayerDefn()  # 图层属性
for index in range(layerdef.GetFieldCount()):
    field_defn = layerdef.GetFieldDefn(index)
    print(field_defn.GetName(), field_defn.GetType(), field_defn.GetWidth())
# 获取要素信息（空间地理信息）
# for idx in range(layer1.GetFeatureCount()):
#     layer1.GetFeature(index)
feature1 = layer1.GetFeature(0)
print(feature1.keys())  # 获取全部属性字段
print(feature1.GetField('AREA'))  # 也可以索引获得
geom = feature1.GetGeometryRef()
print(geom.GetGeometryName())  # 几何要素类型
print(geom.GetGeometryCount())  # 几何要素数量
print(geom.ExportToWkt())  #
print(geom.GetSpatialReference())  # 空间参考信息
# 创建矢量数据
crtshp = driver_shp.CreateDataSource(r'E:\gistest\testdata\ss.shp')
crtlayer = crtshp.CreateLayer('dd', geom_type=ogr.wkbPoint)
# 添加字段
field_df = ogr.FieldDefn('ding', ogr.OFTString)
field_df.SetWidth(5)
crtlayer.CreateField(field_df)
# 添加要素
featuredf = crtlayer.GetLayerDefn()
fet = ogr.Feature(featuredf)
point = ogr.Geometry(ogr.wkbPoint)
point.SetPoint(1, 1, 1)
fet.SetGeometry(point)
fet.SetField('ding', 'wu')
crtlayer.CreateFeature(fet)
crtshp.Destroy()

# 使用ogr wkt创建几何形状
guojiePolygon.Destroy()


# 根据属性和空间关系筛选数据，并存为shp  filter
# layer1.SetAttributeFilter("条件")
# 还可根据空间位置筛选
# layer1.SetSpatialFilter("条件")

# Fiona
with fiona.open(r'E:\gistest\b26573ab\中国主要水系-shp\Taihu.shp') as c:
    print(len(c))
plt.show()
