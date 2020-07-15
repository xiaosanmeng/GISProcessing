#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask, render_template, request, url_for, send_from_directory,jsonify, redirect
import os
import json
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
app = Flask(__name__)

# ALLOWED_EXTENSTIONS = set(['png', 'jpg', 'jpeg', 'gif'])
download_floder = './upload/'

def allow_file(filename):
    allow_list = ['png', 'PNG', 'jpg', 'doc', 'docx', 'txt', 'pdf', 'PDF', 'xls', 'rar', 'exe', 'md', 'zip'] 
    suffix = filename.split('.')
    return len(suffix) > 1 and suffix[1] in allow_list

@app.route('/main')
@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/getlist')
def getlist():
    file_url_list = []
    file_list = os.listdir(download_floder)
    temple = '<a href="./download/{0}">{0}</a>'
    return json.dumps([temple.format(f) for f in os.listdir(download_floder)])

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(download_floder,filename, as_attachment=True)

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']
    result = 'null'
    # print type(file)
    if f and allow_file(f.filename):
        f.save(os.path.join(download_floder, f.filename))
        result = 'OK'
    elif f:
        result = 'NO'
    return render_template('index.html', status=result)


if __name__ == '__main__':
    if not os.path.exists(download_floder):
        os.makedirs(download_floder)
    app.run(debug=True, host='0.0.0.0')
