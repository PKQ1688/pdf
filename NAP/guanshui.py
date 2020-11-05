# -*- coding:utf-8 -*-
# @author :adolf
import pdfplumber
import pandas as pd
import xlwt

pdf_path = "Oct_2020/224920201000059255-A01.pdf"


def get_result(pdf_path):
    pdf = pdfplumber.open(pdf_path)
    res = {"填发日期": "",
           "缴款单号码": "",
           "报关单编码": "",
           "税号": "",
           "货物名称": "",
           "数量": "",
           "单位": "",
           "完税价格": "",
           "税率": "",
           "税款金额": "", }
    for page in pdf.pages:
        # 获取当前页面的全部文本信息，包括表格中的文字
        # print(page.extract_text())
        page_text = page.extract_text()
        text_list = page_text.split('\n')

        for line in text_list:
            # print(line)
            if "填发日期" in line:
                # print('=' * 20)
                content = line.split(' ')
                # print(content)
                res['填发日期'] = content[1].split('：')[1]
                res['缴款单号码'] = content[-1].split('.')[1]
                res['报关单编码'] = res['缴款单号码'].split('-')[0]
                # print('=' * 20)
                break
        # for line in page.extract_text():
        #     print(line)
        table_text = page.extract_tables()[0]
        for table_index in range(len(table_text)):
            row = table_text[table_index]
            if "税 号" in row:
                p_row = list()
                for word in table_text[table_index + 1]:
                    if word is not None:
                        p_row.append(word)
                # print(table_text[table_index + 1])
                # print(p_row)
                res["税号"] = p_row[0].split('\n')
                res["货物名称"] = p_row[1].split('\n')
                res["数量"] = p_row[2].split('\n')
                res["单位"] = p_row[3].split('\n')
                res["完税价格"] = p_row[4].split('\n')
                res["税率"] = p_row[5].split('\n')
                res["税款金额"] = p_row[6].split('\n')

                break
        # print('---------- 分割线 ----------')
    pdf.close()
    res['填发日期'] = [res['填发日期']] * len(res['税号'])
    res['缴款单号码'] = [res['缴款单号码']] * len(res['税号'])
    res['报关单编码'] = [res['报关单编码']] * len(res['税号'])
    # print(res)

    df = pd.DataFrame(res)
    print(df)

    df.to_csv(pdf_path.split("/")[-1].split(".")[0] + ".csv", index=None)


if __name__ == '__main__':
    get_result(pdf_path)
