# -*- coding: utf-8 -*-
# @Time    : 2020/7/15 12:44
# @Author  : ding
# @File    : view.py

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os
from osgeo import ogr, osr
from mpl_toolkits.basemap import Basemap
import folium
from descartes import PolygonPatch
import shapefile as shp
from shapely.geometry import Point

plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus']=False   #这两行需要手动设置

def proj2proj(create_path, layer_name, geom_class, spatial, target, layer):
    '''

    :param create_path: 路径
    :param layer_name: 层名
    :param geom_class: ogr.wkbPolygon
    :param spatial: 原投影
    :param target:  目标投影
    :param layer:  要转换的层
    :return:
    '''
    driver = ogr.GetDriverByName('ESRI Shapefile')
    if os.access(create_path, os.F_OK):
        driver.DeleteDataSource(create_path)
    new_source = driver.CreateDataSource(create_path)
    newlayer = new_source.CreateLayer(layer_name, target, geom_class)

    coord_trans = osr.CoordinateTransformation(spatial, target)
    for index in range(layer.GetFeatureCount()):
        feature = layer.GetFeature(index)
        geom = feature.GetGeometryRef()
        geom.Transform(coord_trans)

        geom = ogr.CreateGeometryFromWkt(geom.ExportToWkt())
        feat = ogr.Feature(newlayer.GetLayerDefn())
        feat.SetGeometry(geom)
        newlayer.CreateFeature(feat)
    new_source.Destroy()


# s = gpd.GeoSeries([Point(0, 1), Point(1, 2), Point(2, 3)])
# df1 = gpd.GeoDataFrame({'geometry': s})
# print(df1)
# df1.plot()
# plt.show()

driver = ogr.GetDriverByName('ESRI Shapefile')
taihu = r'E:\gistest\taihukongjian\taihu.shp'
liuyu = r'E:\gistest\taihukongjian\area.shp'
hedao = r'E:\gistest\taihukongjian\gis\shp\hedao.shp'
hedao2 = r'E:\gistest\taihukongjian\gis\shp\一维河道[分段边界].SHP'

driver = ogr.GetDriverByName('ESRI Shapefile')
taihudataset = driver.Open(taihu)
liuyudataset = driver.Open(liuyu)
hedaodataset = driver.Open(hedao)
hedao2dataset = driver.Open(hedao2)

taihulayer = taihudataset.GetLayer(0)
liuyulayer = liuyudataset.GetLayer(0)
hedaolayer = hedaodataset.GetLayer(0)
hedao2layer = hedao2dataset.GetLayer(0)

liuyu_wkt = liuyulayer.GetSpatialRef()
hedao_wkt = hedaolayer.GetSpatialRef()
hedao2_wkt = hedao2layer.GetSpatialRef()

spatialret_taihu = taihulayer.GetSpatialRef()

create_path = r'E:\gistest\testdata\taihuliuyu.shp'
proj2proj(r'E:\gistest\太湖投影转换\taihuliuyu.shp', 'taihuliuyu', ogr.wkbPolygon, liuyu_wkt, spatialret_taihu, liuyulayer)
proj2proj(r'E:\gistest\太湖投影转换\taihuhedao.shp', 'taihuhedao', ogr.wkbLineString, hedao_wkt, spatialret_taihu, hedaolayer)
proj2proj(r'E:\gistest\太湖投影转换\taihuhedao2.shp', 'taihuhedao2', ogr.wkbLineString, hedao2_wkt, spatialret_taihu, hedao2layer)

fig, ax = plt.subplots(1, 1)
gdf_liuyu = gpd.read_file(r'E:\gistest\testdata\taihuliuyu.shp')
gdf_liuyu['shy'] = range(len(gdf_liuyu))

gdf_taihu = gpd.read_file(r'E:\gistest\taihukongjian\taihu.shp')
gdf_hedao = gpd.read_file(r'E:\gistest\太湖投影转换\taihuhedao.shp')
gdf_hedao1 = gpd.read_file(r'E:\gistest\太湖投影转换\taihuhedao2.shp')

station_info = pd.read_csv('E:\gistest\station_info.csv', index_col=0)
for index in range(len(station_info)):
    if index == 0:
        s = gpd.GeoSeries([Point(station_info.loc[index, 'LGTD'], station_info.loc[index, 'LTTD'])])
    else:
        s = s.append(gpd.GeoSeries([Point(station_info.loc[index, 'LGTD'], station_info.loc[index, 'LTTD'])]))
gdf_point = gpd.GeoDataFrame({'geometry': s})


gdf_liuyu.plot(ax=ax, color='green')
gdf_taihu.plot(ax=ax)
gdf_hedao.plot(ax=ax)
plt.xlim(119, 122)
gdf_point.plot(ax=ax, marker='o', markersize=10, color='blue')
for index, xy in enumerate(zip(station_info.loc[:, 'LGTD'], station_info.loc[:, 'LTTD'])):
    plt.annotate(station_info.loc[index, 'STNM'], xy=xy, xytext=(-2, 2), textcoords='offset points', color='black', fontsize=2)
plt.savefig("test.png", dpi=700, format="png")
plt.show()
