# 这是为了入门学习python对gis的二次开发而创建的一个项目。
- 安装模块
### 下面是一些重要的包
``import geopandas as gpd``

``from shapely.geometry import Point``
``
from pprint import pprint``

``import os``

``from pyproj import P roj  # 主要进行经纬度与坐标之间的转换``

``from pyproj import transform  # 在相同基准面下的两个不同投影的变换  cs2cs``

``from pyproj import Geod  # 计算地球大圆两点间的距离和相对方位，插入等分点等``

``from osgeo import osr  # 处理空间参考信息  创建投影``

``from osgeo import gdal  # 处理栅格数据``

``from osgeo import gdalconst  # 绑定了gdal中的一些常量``

``from osgeo import ogr  # 处理矢量数据``

``import fiona  # 读写 处理矢量数据``

``from PIL import Image  # 栅格数据读写 基于像元``

``import cv2``

``import tifffile``

``import matplotlib.pyplot as plt``

``from mpl_toolkits.basemap import Basemap  # 地图制作``

``import mpl_toolkits.basemap``

``import shapely``

``import sqlite3``

``import numpy as np``

``import shapefile  # pyshp``

``import geojson``

``import folium``

``import geopandas as gpd``
``
***
先就写这些吧！

更新
***