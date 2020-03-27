#!/usr/bin/python3
import hashlib
from random import random

from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from encrypt import encrypt_file

IS_DEBUG = True  # False for release!
UPLOAD_FOLDER = 'videos'
ALLOWED_EXTENSIONS = {'mp4', 'mkv', 'jpg'}
MAX_FILE_SIZE_MB = 512
AES_KEY = 'super_secret_key'  # hashed key should be inserted externally!
# AES_HASH_KEY = hashlib.sha256(AES_KEY.encode('utf-8')).digest()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE_MB * 1024 * 1024


# engine = create_engine('sqlite:///videos.db')
# Base.metadata.bind = engine
#
# DBSession = sessionmaker(bind=engine)
# session = DBSession()

# checking the file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def add_file_to_db():
    pass


def add_file_to_library(filename):
    encrypt_file(AES_KEY, UPLOAD_FOLDER + "/" + filename)
    add_file_to_db()


# upload file main form
@app.route('/', methods=['GET', 'POST'])
def upload_file_form():
    if request.method == 'POST':
        return upload_file()
    return render_template('uploadFile.html', fileTypes=str(ALLOWED_EXTENSIONS)[1:-1], fileSize=MAX_FILE_SIZE_MB)


# upload file
@app.route('/upload_input_content', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        abort(400, 'No file present')
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        add_file_to_library(filename)
        return jsonify({'input_content_id': 1})
    abort(400, 'This video format is not supported ')


if __name__ == '__main__':
    # preparing environment
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app.debug = IS_DEBUG
    app.run(host='0.0.0.0', port=5000)
