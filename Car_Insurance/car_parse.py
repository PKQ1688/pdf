# -*- coding:utf-8 -*-
# @author :adolf
import os
import re
import camelot
import cn2an

pdf_file_path = "pdf_file/"
pdf_list = os.listdir(pdf_file_path)


def parse_pdf(pdf_path):
    res_dict = dict()
    print(pdf_path)
    try:
        tables = camelot.read_pdf(pdf_path)
        content = tables[0].data
    except Exception as e:
        print(e)
        print('----------分割线---------')
        return {"error": "输入票据存在问题", "status": 1}
    for ori_row in content:
        row = list()
        for content in ori_row:
            if content is not None and content != "":
                row.append(content.replace("\n", "").replace(" ", ""))
        if len(row) == 0:
            continue

        row_line = "".join(row)

        if "车架号" in row_line or "车辆识别代码" in row_line:
            if "车架号" in row_line:
                row_line_list = row_line.split('车架号')
            else:
                row_line_list = row_line.split('车辆识别代码')
            res_car = row_line_list[1]

            cop = re.compile("[^a-z^A-Z^0-9]")
            res_car = cop.sub('', res_car)
            # print(res_car)
            res_dict["车架号"] = res_car
        if "年" in row_line and "保险期间" in row_line and "月" in row_line:
            pattern = re.compile("\d+年\d+月\d+日\d+时\d+分")
            result = pattern.findall(row_line)
            # print(result)
            res_dict["保险期间"] = result[0] + '-' + result[1]
        if "保险费合计" in row_line:
            # print(row_line)
            pattern = re.compile("(\d+(\.\d+)?)")  # 查找数字
            result = pattern.findall(row_line)
            if len(result) == 1:
                res_dict["保险费合计"] = result[0][0]
            else:
                pattern2 = re.compile("[壹贰叁肆伍陆柒捌玖拾佰整]{1,}")
                result2 = pattern2.findall(row_line)
                # print(result2)
                output = cn2an.cn2an(result2[0])
                res_dict["保险费合计"] = output
        # for index in range(len(row)):
        #     if "车架号" in row[index]:
        #         res_dict["车架号"] = row[index + 1]
        #     elif "保险期间" == row[index]:
        #         res_dict["保险期间"] = row[index + 1]
        #     elif "保险费合计" in row[index]:
        #         res_dict["保险费合计"] = row[index]

    print(res_dict)
    print('----------分割线---------')
    return res_dict


if __name__ == '__main__':
    for pdf_name in pdf_list:
        pdf_path = os.path.join(pdf_file_path, pdf_name)
        parse_pdf(pdf_path)
        # break
