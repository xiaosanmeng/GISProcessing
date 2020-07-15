# -*- coding: utf-8 -*-
# @Time    : 2020/7/7 10:04
# @Author  : ding
# @File    : 3zhang.py

from osgeo import ogr, osr
import fiona
# osr创建投影信息
# OGR操作矢量数据

file_path = r'E:\gistest\data\400guojiaSHP\国界与省界_label.shp'
china_shp = ogr.Open(file_path)
driver = china_shp.GetDriver()
print(driver.name)
print(dir(china_shp))

driver_ = ogr.GetDriverByName('ESRI Shapefile')
source = driver_.Open(file_path, update=1)
source.Destroy()

# 获取图层信息 layer 是由同种要素组成在一起的层 点线面
layer1 = china_shp.GetLayer(0)
print(layer1.GetFeatureCount())  # 要素个数
print(layer1.GetExtent())  # 空间范围   西东南北四至
layerdef = layer1.GetLayerDefn()  # 图层属性
for i in range(layerdef.GetFieldCount()):
    defn = layerdef.GetFieldDefn(i)
    print(defn.GetName(), defn.GetType())

# 读取要素
feature1 = layer1.GetFeature(0)
print(feature1.keys())
print(feature1.GetField('AREA'))  # 获取字段值
# 遍历属性
for i in range(feature1.GetFieldCount()):
    print(feature1.GetField(i))

# 要素的几何形状geometry
geom = feature1.GetGeometryRef()
print(geom.GetGeometryName())
print(geom.GetGeometryCount())
print(geom.GetPointCount())
print(geom.ExportToWkt())
print(layer1.GetSpatialRef())

# 根据条件选择数据 空间位置筛选
print(layer1.SetAttributeFilter('AREA<50'))
print(layer1.GetFeatureCount())

with fiona.open(r'E:\gistest\data\400guojiaSHP\国界与省界_arc.shp') as f:
    print(f.driver)
    print(f[1])
    print(f.crs)
    print(f.schema)


