# -*- coding:utf-8 -*-
# @author :adolf
import pdfplumber

path = "dzda_101144060100003026492020053021315945_1590845522700.pdf"  # 导入PDF路径
pdf = pdfplumber.open(path)
i = 0
for page in pdf.pages:
    print('第几页{}'.format(i))
    i += 1
    print(page.extract_text())
    print('=================================')
    # for table in page.extract_tables():
    #     # print(table)
    #     for ori_row in table:
    #         row = list()
    #         for cont in ori_row:
    #             if cont is not None:
    #                 row.append(cont)
    #         print(row)
