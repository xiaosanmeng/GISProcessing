# -*- coding: utf-8 -*-
# @Time    : 2020/6/23 15:35
# @Author  : ding
# @File    : test.py

# 【Python处理矢量数据（例shp文件）】
# 1.ogr：GDAL项目中用于处理矢量数据的模块
# 2.fiona：基于ogr的封装，提供了更简洁了API
# 3.geopandas：基于fiona进行封装，并在pandas的基础上添加了对空间数据的支持，实现了读取空间数据以及对空间数据进行处理

# GeoPandas是一个开源项目，它的目的是使得在Python下更方便的处理地理空间数据。
# GeoPandas扩展了pandas的数据类型，允许其在几何类型上进行空间操作。
# 几何操作由 shapely执行。 GeoPandas进一步依赖于 fiona进行文件存取和 descartes ，matplotlib 进行绘图。

# 一个GeoDataFrame是一个列表数据结构，它包含一个叫做包含geometry的列，这个geometry包含一个GeoSeries。
# GeoDataFrame.from_postgis 从PostGIS数据库文件中加载GeoDataFrame。

import geopandas as gpd
# shapely主要是在笛卡尔平面对几何对象进行操作和分析。
# 笛卡尔坐标系（Cartesian coordinates，法语：les coordonnées cartésiennes）就是直角坐标系和斜坐标系的统称。
from shapely.geometry import Point
import shapefile
import contextily as ctx
from geoalchemy2 import Geometry, WKTElement
import matplotlib.pyplot as plt
import pandas as pd
import sqlalchemy
from shapely import geometry
import numpy as np
import adjustText as aT
import matplotlib

# matplotlib.use('Agg')

plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus']=False   #这两行需要手动设置


engine = sqlalchemy.create_engine('postgresql://postgres:postgres@localhost:5432/ding', use_batch_mode=True)
# 空间数据插入数据库
# df = pd.DataFrame()
# size = 300
# df['id'] = range(0, size)
# df['value1'] = np.random.randint(0, 100, size=size)
# df['lon'] = np.random.randint(103000000, 105000000, size=size)/1000000
# df['lat'] = np.random.randint(30000000, 35000000, size=size) / 1000000
# geom = [Point(xy) for xy in zip(df.lon, df.lat)]
# # del df['lon']
# # del df['lat']
# crs = {'init': 'epsg:4326'}
# geodataframe = gpd.GeoDataFrame(df, crs=crs, geometry=geom)
# # 将geodataframe中的geometry转换格式，由于geopandas中使用的是shapley的point格式，
# # 而PostGIS中使用的是geoalchemy2中的point（或者说插入数据需要使用geoalchemy2格式）
# geodataframe['geom'] = geodataframe['geometry'].apply(lambda x: WKTElement(x.wkt, 4326))
# geodataframe.drop('geometry', 1, inplace=True)
# geodataframe.to_sql('test1', engine, if_exists='replace', index=None,
#                     dtype={'geom': Geometry('POINT', 4326)})

# *********************************************************************************************************************

xmin, xmax, ymin, ymax = 105.20285500000001, 111.53544500000002, 31.31264, 39.97756


# print(geometry.Polygon([(0, 0), (0.5, 0.5), (1, 0), (0.5, -0.5)]))


def add_basemap(ax, zoom, url):
    xmin, xmax, ymin, ymax = ax.axis()
    basemap, extent = ctx.bounds2img(
        xmin, ymin, xmax, ymax, zoom=zoom, url=url)
    ax.imshow(basemap, extent=extent, interpolation='bilinear')
    ax.axis((xmin, xmax, ymin, ymax))


# 读取数据
shanxi = gpd.read_file(r'E:\GisLearn\python_basics_for_gis-master\Exercise1\data\shan3xi.json')
hunan = gpd.read_file(r'E:\GisLearn\data\400guojiaSHP\国界与省界_polygon.shp')
print(hunan.columns)
hunan = hunan[(hunan['NAME'] == '湖南省')]
guojieshengjie = gpd.read_file(r'E:\GisLearn\data\400guojiaSHP\国界与省界_arc.shp')
guojieshengjie1 = gpd.read_file(r'E:\GisLearn\data\400guojiaSHP\国界_polygon.shp')
shijie = gpd.read_file(r'E:\GisLearn\data\世界地图shp\World GIS data\country.shp')
dijishi = gpd.read_file(r'E:\GisLearn\data\400guojiaSHP\地级行政界线_arc.shp')
print(dijishi.columns)

df1 = gpd.GeoDataFrame(hunan['geometry'], crs={'init': 'epsg:3857'})
df2 = gpd.GeoDataFrame(guojieshengjie['geometry'], crs={'init': 'epsg:3857'})
new_df = gpd.overlay(guojieshengjie1, shanxi, how='union')
fig, ax = plt.subplots(1, 1)
new_df[new_df.notna().any(axis=1)].plot(ax=ax, color="green")
new_df[new_df.isna().any(axis=1)].plot(ax=ax, color="red")

shenghui = gpd.read_file(r'E:\GisLearn\data\400guojiaSHP\首都和省会_point.shp')
print(shenghui.columns)
text = []

# 合并图层
fig, ax = plt.subplots(1, 1)
shenghui = shenghui[shenghui["NAME"] == '长沙']
for x, y, label in zip(shenghui.geometry.x, shenghui.geometry.y, shenghui["NAME"]):
    text.append(plt.text(x, y, label, fontsize=20))
# aT.adjust_text(text, force_points=0.3, force_text=0.8, expand_points=(1, 1), expand_text=(1, 1),
#                arrowprops=dict(arrowstyle="-", color='grey', lw=0.5))
ss = guojieshengjie1['geometry'].unary_union
s = gpd.GeoSeries([guojieshengjie['geometry'].unary_union, shanxi['geometry'].unary_union, hunan['geometry'].unary_union])
print(type(s))
# gpd.GeoSeries([guojieshengjie1['geometry'].unary_union]).plot(ax=ax, color="lightgrey")
# gpd.GeoSeries([shanxi['geometry'].unary_union]).plot(ax=ax, color="grey")
gpd.GeoSeries([hunan['geometry'].unary_union]).plot(ax=ax, color="grey")
gpd.GeoSeries([shenghui['geometry'].unary_union]).plot(ax=ax, color="red")
# gpd.GeoSeries([dijishi['geometry'].unary_union]).plot(ax=ax, color="grey")
# 保存为矢量图
plt.savefig('E:/test.svg', format='svg')
plt.show()

fig, ax = plt.subplots(1, 1)
# GeoSeries.plot(column=None,colormap=None,alpha=0.5,categorical=False,legend=False,axes=None)
# 绘制GeoDataFrame中几何图形。如果列参数给定，颜色根据这列的值绘制，
# 否则在geometry列调用GeoSeries.plot()函数。都封装在plot_dataframe()函数中。
shanxi.plot(ax=ax, legend=True, column='childNum')
hunan.plot(ax=ax, legend=True)
shanxi_bound = shanxi.bounds
plt.show()

points = pd.read_csv(r"E:\GisLearn\python_basics_for_gis-master\Exercise1\data\pois.txt")
temp = points.head(10)
print(points.columns)
# 经纬度转化为点
points["geometry"] = points.apply(lambda z: Point(z.lng, z.lat), axis=1)

# 需要指定参考坐标系
pois = gpd.GeoDataFrame(points, crs={'init': 'epsg:3857'})
# print(pois.head(5))
pois = pois.dropna()  # 去空值  还是存在非正常点
pois = pois.loc[(pois.lng > xmin) & (pois.lng < xmax) & (pois.lat > ymin) & (pois.lat < ymax)]
# minx, miny, maxx, maxy = pois.boundary
pois.plot(figsize=(10, 10), alpha=0.5, edgecolor='k', column='score')
plt.show()

# to_crs 转换GeoDataFrame的geometry列中的所有几何图形到其他坐标参考系统。
# 当前GeoSeries的crs属性必须被设置。
# crs属性需要被指定以用于输出，或是用字典形式或是用EPSG编码方式。如果inplace=True，
# 在当前的dataframe中geometry列将被替换，否则将返回一个新的GeoDataFrame。
ax = shanxi.to_crs(epsg=3857).plot(figsize=(10, 10), alpha=0.5, edgecolor='k')
add_basemap(ax, zoom=10,
            url=ctx.providers.Stamen.Watercolor)

# to_file 将GeoDataFrame写入文件。默认情况下，写成ESRI的shapefile格式。
# 但是通过Fiona，任何OGR数据源也被支持写入。**kwargs被传给Fiona驱动器。
# GeoSeries.to_json(**kwargs) 将GeoDataFrame以字符串的方式表示为GeoJSON对象返回。

# ax = shanxi.to_crs(epsg=3857).plot(figsize=(10, 10), alpha=0.5, edgecolor='k')
# pois.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, edgecolor='green')
# add_basemap(ax, zoom=10,
#             url="http://webrd01.is.autonavi.com/appmaptile?x={x}&y={y}&z={z}&lang=zh_cn&size=1&scale=1&style=8")
plt.show()
print('pass')
