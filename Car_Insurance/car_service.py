# -*- coding:utf-8 -*-
# @author :adolf
import os
import json
from flask import Flask
from flask import request
import traceback
from flask_cors import CORS
import base64
# import cv2
# import numpy as np
import uuid
from Car_Insurance.car_parse import parse_pdf

"""
support PDF process reconstruction
"""
app = Flask(__name__)
CORS(app, resources=r'/*')


# def base64_to_opencv(image_base64):
# img = base64.b64decode(image_base64)
# img_array = np.frombuffer(img, np.uint8)
# img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
# return img


@app.route('/pdf_parse_service/', methods=["post"], strict_slashes=False)
def service_main():
    try:
        in_json = request.get_data()
        if in_json is not None:
            in_dict = json.loads(in_json.decode("utf-8"))
            pdf_base = in_dict["image"]
            uid = uuid.uuid4()
            with open("{}.pdf".format(uid), "wb") as f:
                f.write(base64.b64decode(pdf_base))
            # result_dict['result'] = result
            result = parse_pdf("{}.pdf".format(uid))
            result_dict = dict()
            result_dict['result'] = result
            result_dict["status"] = 0
            os.remove("{}.pdf".format(uid))
            return json.dumps(result, ensure_ascii=False)
        else:
            return json.dumps({"error_msg": "data is None", "status": 1}, ensure_ascii=False)
    except Exception as e:
        traceback.print_exc()
        return json.dumps({"error_msg": "unknown error:" + repr(e), "status": 1}, ensure_ascii=False)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2003, debug=True)
