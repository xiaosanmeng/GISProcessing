# -*- coding: utf-8 -*-
# @Time    : 2020/6/24 14:01
# @Author  : ding
# @File    : shp2postgresql.py

# coding:utf-8
import geopandas as gpd
import pandas as pd
from sqlalchemy import create_engine
from geoalchemy2 import Geometry, WKTElement
import numpy as np
import os
import re
import json
from osgeo import ogr


def write_gis(path, engine):
    geoType = getGeoTypeFromDir(path)
    # 判断点线多边形
    if (geoType):
        map_data = gpd.GeoDataFrame.from_file(path)
        map_data['geometry'] = map_data['geometry'].apply(lambda x: WKTElement(x.wkt, 3857))
        # map_data['geometry'] = map_data['geometry']
        # map_data.drop(['center','parent'], axis = 1, inplace=True)
        # name = re.split('\\.', path)[0]
        # map_data['geom'] = map_data['geometry'].apply(lambda x: WKTElement(x.wkt, 3857))
        # map_data.drop('geometry', 1, inplace=True)
        map_data.to_sql(
            name='%s' % geoType,
            con=engine,
            if_exists='replace',
            dtype={'geometry': Geometry(geometry_type='GEOMETRY', srid=3857)})
        return 'success'


# 创建批量任务
def to_do(file_path, username, password, dbname):
    link = "postgresql://{0}:{1}@localhost:5432/{2}".format(username, password, dbname)
    print(file_path)
    engine = create_engine(link, encoding='utf-8')
    file_list = os.listdir(file_path)
    # print(file_list)
    # a = os.path.join(file_path, file_list[0])
    for x in file_list:
        write_gis(os.path.join(file_path, x), engine)
    # write_gis(file_path, engine)
    # map(lambda x: write_gis(os.path.join(file_path, x), engine), file_list)
    return 'over!'


# 从文件夹中读取shp，获得其类型
def getGeoTypeFromDir(dirPath):
    """从文件夹中读取shp，获得其类型"""
    ext = os.path.splitext(dirPath)[1]
    if (ext == '.shp'):
        driver = ogr.GetDriverByName('ESRI Shapefile')
        file = dirPath  # 返回文件的绝对路径，这里返回的是错的，缺少了上级文件夹
        # names = os.path.split(file)
        # file = os.path.join(names[0], dirPath, names[1])
        # 使用OGR打开一个矢量数据，如shp文件或GeoJSON文件，会产生一个DataSource对象。
        # 该对象包含若干个Layer，每个Layer就是一个要素集。
        # 值得注意的是，大多数矢量数据格式一般只有一个Layer，少数有多个（如SpatiaLite格式）。
        # 既然Layer是个要素集，可想而知它包含的就是一个个的feature了。
        # Feature的概念稍微学过GIS原理的朋友应该都知道，Arcmap里也经常提到，就是几何对象和属性表的集和。
        # 所以，feature包含的就是geometry和attribute。

        # 也可以直接使用ogr.open函数打开文件。该函数会根据文件后缀名自动选择driver进行数据读取。
        dataSource = driver.Open(file, 0)
        print(type(dataSource))
        # 获取layer
        # OGR的Layer概念类似于ArcGIS里的FeatureClass，就是多个同类要素(点、线、多边形)的集和。
        layer = dataSource.GetLayer(0)
        # 0为几何要素特征
        feat = layer.GetFeature(1)

        geom = feat.GetGeometryRef()
        # print(dir(geom))
        # print(geom.GetGeometryName())


        geoCode = geom.GetGeometryType()
        print(geoCode)
        return geom.GetGeometryName()
    else:
        return None


# 解译ogr的geometry code
def deGeoTypeCode(code):
    """解译ogr的geometry code"""
    if code == 1:
        return 'POINT'
    elif code == 2:
        return 'LINESTRING'
    elif code == 3:
        return 'POLYGON'
    return None


def shp2pgsql(file, engine):
    """单个shp文件入库"""
    file_name = os.path.split(file)[1]
    print('正在写入:'+file)
    tbl_name = file.split('\\')[-2].replace(' ', '').lower() + file_name.split('.')[0]  # 表名
    map_data = gpd.GeoDataFrame.from_file(file)
    # spatial_ref = map_data.crs.srs.split(':')[-1]  # 读取shp的空间参考
    map_data['geometry'] = map_data['geometry'].apply(
        lambda x: WKTElement(x.wkt, 3857))
    # geopandas 的to_sql()方法继承自pandas, 将GeoDataFrame中的数据写入数据库
    map_data.to_sql(
        name=tbl_name,
        con=engine,
        if_exists='replace', # 如果表存在，则替换原有表
        chunksize=1000,  # 设置一次入库大小，防止数据量太大卡顿
        # 指定geometry的类型,这里直接指定geometry_type='GEOMETRY'，防止MultiPolygon无法写入
        dtype={'geometry': Geometry(
            geometry_type='GEOMETRY', srid=3857)},
        method='multi'
    )
    return None


def shp2pgsql_batch(dir_name, engine):
    """创建批量任务"""
    os.chdir(dir_name)  # 改变当前工作目录到指定路径
    # engine = create_engine(username, password, host, port, dbname)
    file_list = os.listdir(dir_name)
    # for file in file_list:
    #     cur_path = os.path.join(dir_name, file)
    # if os.path.isdir(cur_path):

    for file in file_list:
        if file.split('.')[-1] == 'shp':
            file = os.path.abspath(file)
            shp2pgsql(file, engine)
    return None


def pgsql2shp(engine):
    sql1 = '''select * from WorldGISdatarivers'''
    s = gpd.read_postgis(sql1, con=engine, geom_col='geometry')
    return s


# 执行任务计划
if __name__ == '__main__':
    file_path1 = r'E:\GisLearn\data\世界地图shp\World GIS data\country.shp'
    file_path = r'E:\GisLearn\data\世界地图shp\World GIS data'
    username = 'postgres'
    password = 'postgres'
    dbname = 'ding'
    # to_do(file_path, username, password, dbname)
    link = "postgresql://{0}:{1}@localhost:5432/{2}".format(username, password, dbname)
    engine = create_engine(link, encoding='utf-8')
    # shp2pgsql(file_path, engine)
    shp2pgsql_batch(file_path, engine)
    pgsql2shp(engine)
