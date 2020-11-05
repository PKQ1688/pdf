# -*- coding:utf-8 -*-
# @author :adolf
import requests
import json
import base64

file_path = 'pdf_file/test_1.pdf'


def get_result(encodestr):
    payload = {"image": encodestr}
    r = requests.post("http://localhost:2003/pdf_parse_service/", json=payload)
    # print(r.text)
    res = json.loads(r.text)
    return res


with open(file_path, 'rb') as f:
    image = f.read()
    encodestr = str(base64.b64encode(image), 'utf-8')

res_ = get_result(encodestr)
print(res_)
