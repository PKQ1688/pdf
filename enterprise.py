# -*- coding:utf-8 -*-
# @author :adolf
import pdfplumber
from enterprise_json import Enterprise_class_dict
from enterprise_json import right_name, last_name

res_dict = dict()
pdf_path = "pdf_file/enterprise.pdf"

class_2_to_1_dict = dict()
for key, value in Enterprise_class_dict.items():
    # print(key, value)
    for sec_class in value:
        class_2_to_1_dict[sec_class] = key
print(class_2_to_1_dict)
with pdfplumber.open(pdf_path) as pdf:
    key_2_class = "身份标识"
    key_1_class = class_2_to_1_dict[key_2_class]
    flag_row = None
    page_index = 0
    res_other_list = list()
    for page in pdf.pages[:95]:
        # print(page.extract_text())
        for table in page.extract_tables():
            for ori_row in table:
                row = list()
                for cont in ori_row:
                    if cont is not None:
                        row.append(cont)

                        if '\n' in cont:
                            cont_list = cont.split('\n')
                            for one_cont in cont_list:
                                if one_cont in class_2_to_1_dict:
                                    key_2_class = one_cont
                                    key_1_class = class_2_to_1_dict[key_2_class]
                        elif cont in class_2_to_1_dict:
                            key_2_class = cont
                            key_1_class = class_2_to_1_dict[key_2_class]

                if len(row) == 0:
                    continue
                if row[0] == "2\nh" or \
                        "ttp://154.211.28.25/cqs/cqsQeQuery/query/qecredit/localReport" in row[0]:
                    continue
                if len(row) == 1 and row[0] == "":
                    continue
                if len(set(row)) == 1 and list(set(row))[0] == "":
                    continue
                print(row)

                row_use_flag = False

                if key_1_class not in res_dict:
                    res_dict[key_1_class] = dict()
                if key_2_class not in res_dict[key_1_class]:
                    res_dict[key_1_class][key_2_class] = dict()

                if flag_row is not None:
                    for i in range(len(flag_row)):
                        if flag_row[i] is None:
                            continue
                        res_dict[key_1_class][key_2_class][flag_row[i].replace('\n', '')] = row[i].replace('\n', '')
                        row_use_flag = True

                    flag_row = None

                if key_1_class == "附件2：财务报表信息":
                    current_page = "页数_" + str(page_index)
                    # print(current_page)
                    if current_page not in res_dict[key_1_class]:
                        res_dict[key_1_class][current_page] = dict()
                        row_use_flag = True

                    for index in range(0, len(row) - 1, 2):
                        # if row[index] == "2\nh" or "ttp://154.211.28.25/cqs/cqsQeQuery/query/qecredit/localReport" :
                        #     continue
                        res_dict[key_1_class][current_page][row[index]] = row[index + 1]
                        row_use_flag = True

                else:
                    for index in range(len(row)):
                        if row[index] in right_name:
                            res_dict[key_1_class][key_2_class][row[index]] = row[index + 1]
                            row_use_flag = True

                        elif row[index] in last_name:
                            flag_row = row

                if not row_use_flag:
                    if res_dict[key_1_class]['其他'] is None:
                        res_dict[key_1_class]['其他'] = list()
                    res_dict[key_1_class]['其他'].append(row)
        page_index += 1
    # res_dict["其他"] = res_other_list
print(res_dict)
