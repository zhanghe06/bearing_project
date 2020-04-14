#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: file_system.py
@time: 2020-04-14 15:03
"""

# source .venv/bin/activate
# export FLASK_APP=file_system.py
# flask run -h 0.0.0.0
#  * Running on http://127.0.0.1:5000/

from __future__ import unicode_literals

import os

from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_PATH, 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xls', 'xlsx', 'doc', 'docx', 'ppt', 'pptx'}

app = Flask(
    __name__,
    static_folder='uploads',
    static_url_path='/files',
)
app.config['DEBUG'] = True
# flash message 功能需要 SECRET_KEY
app.config['SECRET_KEY'] = '\x03\xabjR\xbbg\x82\x0b{\x96f\xca\xa8\xbdM\xb0x\xdbK%\xf2\x07\r\x8c'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route('/')
def index():
    return '''
    <ul>
        <li><a href="%s" target="_blank">%s</a></li>
    </ul>
    ''' % (
        url_for('downloads'),
        url_for('downloads'),
    )


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads', methods=['GET', 'POST'])
def uploads():
    """文件上传"""
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        request_file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if request_file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if request_file and allowed_file(request_file.filename):
            filename = secure_filename(request_file.filename)
            request_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('downloads', filename=filename))
        else:
            flash('Extension not allowed')
            return redirect(request.url)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/downloads/', methods=['GET', 'POST'])
@app.route('/downloads/<path:subdir>/', methods=['GET', 'POST'])
def downloads(subdir=''):
    """文件上传下载"""
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        request_file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if request_file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if request_file and allowed_file(request_file.filename):
            filename = secure_filename(request_file.filename)
            cur_abs_dir = os.path.join(app.config['UPLOAD_FOLDER'], subdir)
            print(os.path.join(cur_abs_dir, filename))
            request_file.save(os.path.join(cur_abs_dir, filename))
            return redirect(url_for('downloads', subdir=subdir))
        else:
            flash('Extension not allowed')
            return redirect(request.url)
    file_html = '''
    <!doctype html>
    <title>Uploads File</title>
    <h3>Uploads File</h3>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
    # subdir = secure_filename(subdir)
    cur_abs_dir = os.path.join(app.config['UPLOAD_FOLDER'], subdir)
    for root, dirs, files in os.walk(cur_abs_dir, topdown=True):
        print(root, dirs, files)
        files.sort()
        files.reverse()
        # files.sort(reverse=True)
        # 目录
        if dirs:
            file_html += '<div>'
            file_html += '<span>目录</span>'
            file_html += '<ul>'
            for dir_name in dirs:
                file_html += '<li>'
                file_html += '<a href="%s">' % url_for('downloads', subdir=os.path.join(subdir, dir_name))
                file_html += dir_name
                file_html += '</a>'
                file_html += '</li>'
            file_html += '</ul>'
            file_html += '</div>'
        # 文件
        if files:
            file_html += '<div>'
            file_html += '<span>文件</span>'
            file_html += '<ul>'
            for file_name in files:
                file_html += '<li>'
                file_html += '<a href="%s" target="_blank">' % url_for('static',
                                                                       filename=os.path.join(subdir, file_name))
                file_html += file_name
                file_html += '</a>'
                file_html += '</li>'
            file_html += '</ul>'
            file_html += '</div>'
        break
    return file_html
