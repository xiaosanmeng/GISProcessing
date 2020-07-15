#coding:utf-8
from flask import Flask
from gisflaskMaster.main import app

app.config.from_pyfile('settings.py')
from gisflaskMaster.geomodule import views
# import sys;
# sys.path.insert(0,'/Users/jinming/Library/Mobile\ Documents/com\~apple\~CloudDocs/ysj/flask-base/dm/python-flask/data_management/geomodule/gdal')
