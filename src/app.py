from flask import Flask, request, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os

import cv2
import numpy as np


UPLOAD_FOLDER = '/var/hrobbin/tmp/'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])

def count_pixels(image, range):
    value = np.count_nonzero(np.all(image==range, axis=2))
    return value
    
def count_black_white(file):
    img = cv2.imread(file)
    find_white = [255, 255, 255]
    find_black = [0, 0, 0]
    white = count_pixels(img, find_white)
    black = count_pixels(img, find_black)
    return {'black': black, 'white': white}

def hex_to_rgb(hex):
    hex.lstrip('#')
    return list(int(hex[i:i+1], 16) for i in [0, 2, 4])

def count_pixels_by_hex(hex, file):
    rgb = hex_to_rgb(hex)
    img = cv2.imread(file)
    return count_pixels(img, rgb)

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
            count = count_black_white('./tmp/'+filename)
            pixels_black_and_white = 'White pixels: ' + str(count['white']) + ', black pixels: ' + str(count['black'])
            pixels_custom = request.form.get('hex')
            # pixels_custom = count_pixels_by_hex(request.files['hex'])
        else:
            pixels_custom = 0
        return render_template('index.html', pixels=pixels_black_and_white, pixels_custom=pixels_custom)
    else: return render_template('index.html')
app.run(host='0.0.0.0', port=8090)