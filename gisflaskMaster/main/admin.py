# -*- coding: utf-8 -*-
"""
    管理员
"""
import os
import uuid
from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, send_from_directory
from flask_login import login_required, current_user

from gisflaskMaster.main.extensions import db
from gisflaskMaster.main.utils import redirect_back
from gisflaskMaster.main import app
from werkzeug.utils import secure_filename
from functools import wraps


def test(func):
    @wraps(func)
    @app.route('/file/new', methods=['GET', 'POST'])
    @login_required
    def new_file():
        if request.method == 'POST':
            f = request.files.get('file')
            f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
        return render_template('new_file.html')
