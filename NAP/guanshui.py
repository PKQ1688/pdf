# -*- coding:utf-8 -*-
# @author :adolf
import pdfplumber
import pandas as pd
import xlwt

# pdf_path = "Oct_2020/224920201000059894-A01.pdf"


def one_page(page):
    page_text = page.extract_text()
    text_list = page_text.split('\n')
    res = {}
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

            res['填发日期'] = [res['填发日期']] * len(res['税号'])
            res['缴款单号码'] = [res['缴款单号码']] * len(res['税号'])
            res['报关单编码'] = [res['报关单编码']] * len(res['税号'])

            break

    return res


def get_result(pdf_path):
    pdf = pdfplumber.open(pdf_path)
    all_result = list()
    # res = dict()
    page_index = 0
    for page in pdf.pages:
        res_page = one_page(page)
        # print(page_index)
        # print(res_page)
        res = dict()
        res["page"] = page_index
        res["result"] = res_page
        # print(res)
        all_result.append(res)
        # res = dict()
        # print('--------------------')
        # print(all_result)
        # print('--------------------')
        page_index += 1

    # print('---------- 分割线 ----------')

    pdf.close()

    # print(all_result)

    return all_result


# df = pd.DataFrame(res)
# print(df)
#
# df.to_csv(pdf_path.split("/")[-1].split(".")[0] + ".csv", index=None)
def get_excel(pdf_path):
    writer = pd.ExcelWriter(pdf_path.split("/")[-1].split(".")[0] + ".xlsx")
    all_result = get_result(pdf_path)
    for index in range(len(all_result)):
        print(index)
        print(all_result[index])
        df = pd.DataFrame(all_result[index]['result'])
        df.to_excel(writer, sheet_name="Sheet" + str(index), index=False)
        # break
    writer.save()


if __name__ == '__main__':
    # get_result(pdf_path)
    import argparse

    parser = argparse.ArgumentParser(description="Params to use fro train algorithm")

    parser.add_argument("--pdf_path", "-pdf", type=str,
                        default="Oct_2020/224920201000059894-A01.pdf", nargs='?', help="what scenes this model used")
    args = parser.parse_args()

    get_excel(args.pdf_path)
