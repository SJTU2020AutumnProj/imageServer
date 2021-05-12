import base64

import cv2
from flask import jsonify
from flask import Flask
from flask import request
from pyimagesearch.scan import image_scan
from flask_cors import *
import numpy as np
import check


def cv2_base64(image):
    image1 = cv2.imencode('.png', image)[1]
    base64_str = str(base64.b64encode(image1))[2:-1]
    return base64_str


def base64_cv2(base64_str):
    imgString = base64.b64decode(base64_str)
    nparr = np.frombuffer(imgString, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return image


def getImageVar(image):
    img2gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imageVar = cv2.Laplacian(img2gray, cv2.CV_64F).var()
    return imageVar


app = Flask(__name__)
CORS(app, supports_credentials=True)  # 设置跨域


@app.route("/clear", methods=['GET', 'POST'])
def clear():
    data = request.get_json()
    img = data['data'].split(',')[1]

    cv2img = base64_cv2(img)
    wraped = image_scan(cv2img)
    cv2.imshow("Image1", wraped)  # 显示图片
    base64img = cv2_base64(wraped)

    return jsonify({"image": "data:image/png;base64," + base64img})


@app.route("/check", methods=['GET', 'POST'])
def check():
    data = request.get_json()
    img = data['data'].split(',')[1]

    cv2img = base64_cv2(img)

    score = getImageVar(cv2img)

    return jsonify({"score": score})


if __name__ == "__main__":
    app.run()
