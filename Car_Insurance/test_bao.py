# -*- coding:utf-8 -*-
# @author :adolf
import pdfplumber

pdf_path = 'pdf_file/众诚汽车保险股份有限公司.pdf'
pdf = pdfplumber.open(pdf_path)

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        print(page.extract_text())
