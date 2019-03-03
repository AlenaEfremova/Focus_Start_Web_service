import os
import cv2
import numpy as np
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = os.path.basename('upload')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def calc_of_pixels(img):
    """"Сравнивается количество белых и черных пикселей"""
    n_white_pix = np.sum(img == 255)
    n_black_pix = np.sum(img == 0)

    if n_white_pix > n_black_pix:
        res_of_calc = 'Количество белых пикселей в изображении больше, чем черных'
    elif n_black_pix > n_white_pix:
        res_of_calc = 'Количество черных пикселей в изображении больше, чем белых'
    else:
        res_of_calc = 'В загруженном изображении нет черных и белых пикселей'
    return res_of_calc

@app.route('/')
def upload_file():
    """Вывод страницы index.html из папки templates"""
    return render_template('index.html')

@app.route('/result', methods=['GET', 'POST'])
def result_calc():
    """Вывод страницы result.html с результатом сравнения"""
    if request.method == 'POST':
        file = request.files['file']
        filename = os.path.join(app.config['UPLOAD_FOLDER'],
                                secure_filename(file.filename))
        file.save(filename)
        img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
        return render_template('result.html',
                               pixels=calc_of_pixels(img))

if __name__ == '__main__':
    app.run(debug=True)
 