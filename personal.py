# -*- coding:utf-8 -*-
# @author :adolf
import pdfplumber
from personal_json import First_Class_match
from personal_json import last_row_key_list

pdf_path = "pdf_file/personal.pdf"

res_dict = dict()

# class_key_list = First_Class_match.keys()
class_sec_key_list = list()
# for key, value in First_Class_match.items():
#     if isinstance(value, dict):
#         class_sec_key_list.extend(value.keys())
#
# print(class_sec_key_list)
class_1_to_2_dict = dict()
class_2_to_1_dict = dict()

for key, value in First_Class_match.items():
    class_1_to_2_dict[key] = value.keys()
    class_sec_key_list.extend(list(value.keys()))
    for sec_class in value.keys():
        class_2_to_1_dict[sec_class] = key

# print(class_1_to_2_dict)
print(class_2_to_1_dict)

with pdfplumber.open(pdf_path) as pdf:
    row_index = 0
    flag_row = None
    b_flag_row = None
    key_1_class = '基础'
    key_2_class = '基础信息'
    change_class_flag = False
    for page in pdf.pages:
        # print(page.extract_text())
        for table in page.extract_tables():
            for ori_row in table:
                row = list()
                row_use_flag = False
                # res_other_list = list()
                for cont in ori_row:
                    if cont is not None:
                        row.append(cont)

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
                if row[0] is not None and '）' in row[0]:
                    row_cut = None
                    if '\n' in row[0]:
                        row1_word_list = row[0].split('\n')
                        for row1_word in row1_word_list:
                            if '）' in row1_word:
                                row_cut = row1_word
                    elif '）' in row[0]:
                        row_cut = row[0]
                    if row_cut.split('）')[1] in class_sec_key_list:
                        key_2_class = row_cut.split('）')[1]
                        key_1_class = class_2_to_1_dict[key_2_class]
                        change_class_flag = True
                    else:
                        change_class_flag = False

                if key_1_class not in res_dict:
                    res_dict[key_1_class] = dict()
                if key_2_class not in res_dict[key_1_class]:
                    res_dict[key_1_class][key_2_class] = dict()

                if flag_row is not None:
                    for i in range(len(flag_row)):
                        if flag_row[i] is None:
                            continue

                        res_dict[key_1_class][key_2_class][flag_row[i]] \
                            = row[i].replace('\n', '')
                        row_use_flag = True
                    flag_row = None

                if b_flag_row is not None:
                    # if row[]
                    for content in row:
                        if content is None:
                            continue

                    if row[0] is not None and row[0].isdigit():
                        for i in range(len(b_flag_row)):
                            # print(row[0])
                            if b_flag_row[i] not in res_dict[key_1_class][key_2_class]:
                                res_dict[key_1_class][key_2_class][b_flag_row[i]] = list()

                            if b_flag_row[i] is None:
                                continue
                            res_dict[key_1_class][key_2_class][b_flag_row[i]].append(row[i].replace('\n', ''))
                            row_use_flag = True
                    else:
                        b_flag_row = None

                for content in row:
                    if content is None:
                        continue
                    # print(content)
                    if "：" in content:
                        res_dict[key_1_class][key_2_class][content.split('：')[0]] = content.split('：')[1]
                        row_use_flag = True

                    elif content in last_row_key_list and flag_row is None:
                        flag_row_index = row_index
                        flag_row = row

                    elif content == "编号":
                        b_flag_index = row_index
                        b_flag_row = row

                    elif not change_class_flag:
                        pass

                if not row_use_flag:
                    if "其他" not in res_dict[key_1_class]:
                        res_dict[key_1_class]['其他'] = list()
                    res_dict[key_1_class]['其他'].append(row)

                row_index += 1

print(res_dict)
