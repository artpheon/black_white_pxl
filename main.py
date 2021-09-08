from flask import Flask, request, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os

import cv2
import numpy as np


UPLOAD_FOLDER = '/home/hrobbin/python/shift_cft/tmp'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])

def count_pixels(fname):
    img = cv2.imread(fname)
    white = np.sum(img == 255)
    black = np.sum(img == 0)
    return {'black': black, 'white': white}
    

def start_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.secret_key = "super secret key"

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route('/', methods=['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
            if 'file' not in request.files:
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                pix = count_pixels('./tmp/'+filename)
                pixels = 'White pixels: ' + str(pix['white']) + ', black pixels: ' + str(pix['black'])
                return render_template('index.html', pixels=pixels)
        return render_template('index.html')
    
    app.run(host='0.0.0.0', port=8090)

if __name__ == '__main__':
    start_app()