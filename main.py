import base64

import cv2
from flask import jsonify
from flask import Flask
from flask import request
from pyimagesearch.scan import image_scan
from flask_cors import *
import numpy as np


def cv2_base64(image):
    image1 = cv2.imencode('.png', image)[1]
    base64_str = str(base64.b64encode(image1))[2:-1]
    return base64_str


def base64_cv2(base64_str):
    imgString = base64.b64decode(base64_str)
    nparr = np.frombuffer(imgString, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return image


app = Flask(__name__)
CORS(app, supports_credentials=True)  # 设置跨域


@app.route("/", methods=['GET', 'POST'])
def index():
    data = request.get_json()
    img = data['data'].split(',')[1]

    cv2img = base64_cv2(img)
    wraped = image_scan(cv2img)
    cv2.imshow("Image1", wraped)  # 显示图片
    base64img = cv2_base64(wraped)

    return jsonify({"image": "data:image/png;base64," + base64img})


if __name__ == "__main__":
    app.run(debug=True)
