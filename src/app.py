from flask import Flask, request, render_template, redirect
from werkzeug.utils import secure_filename
import os

import cv2
import numpy as np


UPLOAD_FOLDER = '/var/hrobbin/tmp/'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])

def count_pixels(image, range):
    value = np.count_nonzero(np.all(image==range, axis=2))
    return value

def hex_to_rgb(hex):
    ret = list(int(hex[i:i+2], 16) for i in [0, 2, 4])
    return ret
    
def count_black_white(file):
    img = cv2.imread(file)
    find_white = [255, 255, 255]
    find_black = [0, 0, 0]
    white = count_pixels(img, find_white)
    black = count_pixels(img, find_black)
    return {'black': black, 'white': white}

def count_pixels_by_hex(hex, file):
    rgb = hex_to_rgb(hex)
    img = cv2.imread(file)
    return count_pixels(img, rgb)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "super secret key"
app.static_folder = 'static'

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
            filename = app.config['UPLOAD_FOLDER'] + filename
            count = count_black_white(filename)
            wh = count['white']
            bl = count['black']
            if wh > bl:
                pixels_black_and_white = 'Image contains more white({}) pixels, than black({})'.format(wh, bl)
            elif bl > wh:
                pixels_black_and_white = 'Image contains more black({}) pixels, than white({})'.format(bl, wh)
            else:
                pixels_black_and_white = 'Image contains equal amount of black and white pixels: {}'.format(bl)
            hex = str(request.form.get('hex'))
            rgb = count_pixels_by_hex(hex, filename)
            pixels_custom = "Image contains {} pixels of {} colour".format(rgb, hex)
        else:
            pixels_custom = "N/A"
        return render_template('index.html', pixels=pixels_black_and_white, pixels_custom=pixels_custom)
    else: return render_template('index.html')
app.run(host='0.0.0.0', port=8090)