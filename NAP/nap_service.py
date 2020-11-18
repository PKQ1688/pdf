# -*- coding:utf-8 -*-
# @author :adolf
import cv2
import json
from flask import Flask
from flask import request
import traceback
from flask_cors import CORS
from NAP.guanshui import one_page
import pdfplumber
import base64
import uuid

"""
support ocr服务
"""
app = Flask(__name__)
CORS(app, resources=r'/*')


@app.route('/NAP_ocr_service/', methods=["post", "get"], strict_slashes=False)
def service_main():
    try:
        in_json = request.get_data()
        if in_json is not None:
            in_dict = json.loads(in_json.decode("utf-8"))
            pdf_with_base64 = in_dict['image']

            uid_pdf = uuid.uuid4()
            with open("{}.pdf".format(uid_pdf), "wb") as fw:
                fw.write(base64.b64decode(pdf_with_base64))

            pdf = pdfplumber.open("{}.pdf".format(uid_pdf))

            result_dict = dict()
            for page in pdf.pages:
                res_page = one_page(page)
                # result_dict['result'] = res_page["result"]
                for i in range(len(res_page["填发日期"])):
                    # print(i)
                    tmp_dict = dict()
                    for key in res_page:
                        tmp_dict[key] = res_page[key][i]
                    result_dict[str(i)] = tmp_dict

            print(result_dict.keys())
            return json.dumps(result_dict, ensure_ascii=False)
        else:
            return json.dumps({"error_msg": "data is None", "status": 1}, ensure_ascii=False)
    except Exception as e:
        traceback.print_exc()
        return json.dumps({"error_msg": "unknown error:" + repr(e), "status": 1}, ensure_ascii=False)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2003, debug=True)
