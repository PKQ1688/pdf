# -*- coding:utf-8 -*-
# @author :adolf
import pdfplumber
import pandas as pd
import xlwt
import collections
import re


# pdf_path = "Oct_2020/224920201000059894-A01.pdf"


def one_page(page):
    start_index = 0
    page_text = page.extract_text()
    text_list = page_text.split('\n')
    res = collections.defaultdict(list)
    end_index = len(text_list)
    for line_index in range(len(text_list)):
        # print(line_index)
        line = text_list[line_index]
        print(line)

        if "*****" in line:
            # print('=====================')
            dan_num_list = line.split(' ')[1:-1]
            dan_num_list = [dan_num[0] for dan_num in dan_num_list]
            # print(dan_num_list)
            dan_num = "".join(dan_num_list)
            # print(dan_num)
            res["报关单号"].append(dan_num)
        if len(re.findall(r'\*[0-9]*\*', line)) > 0:
            dan_num = line.replace("*", "")
            # print(dan_num)
            res["报关单号"].append(dan_num)

        if "项号" in line:
            start_index = line_index + 1

        if "特殊关系确认" in line:
            end_index = line_index
            line_list = line.split(' ')
            # print(line_list)
            res_line = ["特殊关系确认", "价格影响确认", "支付特许权使用费确认", "自报自缴"]
            line_list = [word.replace(":", "：") for word in line_list if word != ""]
            # print(line_list)
            for i in range(len(res_line)):
                res[res_line[i]].append(line_list[i].split("：")[1])

    # print(res)
    for index in range(start_index, end_index, 3):
        # print(text_list[index])
        # print(text_list[index + 1])
        # print(text_list[index + 2])

        # text_list[index] = text_list[index + 1].replace("及", "|")
        # text_list[index + 1] = text_list[index + 1].replace("及", "|")
        # text_list[index + 2] = text_list[index + 2].replace("及", "|")
        text_list_index_0 = text_list[index].split(' ')
        # print(11111, text_list_index_0)
        if not text_list_index_0[1].isdigit():
            nums = re.findall(r'[0-9]*', text_list_index_0[1])
            nums = [word for word in nums if word != ""]
            # if len(num_) == 1:
            if len(nums) > 1:
                tmp = text_list_index_0[1]
                for num in nums:
                    tmp = tmp.replace(num, "")
                tmp += "|"
                for num in nums[1:]:
                    tmp += num
                    tmp += "|"
                text_list_index_0.insert(2, tmp)
            else:
                text_list_index_0.insert(2, text_list_index_0[1].replace(nums[0], ""))
            text_list_index_0[1] = nums[0]

        # print(2222222, text_list_index_0)
        text_list_index_1 = text_list[index + 1].split(' ')

        text_list_index_1 = handle_something(text_list_index_1)
        # print(text_list_index_1)
        text_list_index_2 = text_list[index + 2].split(' ')

        text_list_index_2 = handle_something(text_list_index_2)
        print(text_list_index_2)
        flag = 0
        if len(text_list_index_2) == 2:
            flag = 1
        # print(text_list_index_1[0])
        if text_list_index_1[0].isdigit():
            if flag:
                info_str = text_list_index_0[2] + '|' + text_list_index_1[1]
            else:
                info_str = text_list_index_0[2] + '|' + text_list_index_1[1] + '|' + text_list_index_2[0]
            res['商品编码'].append(text_list_index_0[1] + text_list_index_1[0])
        else:
            if flag:
                info_str = text_list_index_0[2] + '|' + text_list_index_1[0]
            else:
                info_str = text_list_index_0[2] + text_list_index_1[0] + text_list_index_2[0]
            res['商品编码'].append(text_list_index_0[1])

        # print(info_str)
        res['项号'].append(text_list_index_0[0])
        info_str = info_str.replace('及', '|')
        info_list = info_str.split('|')
        info_list = [word for word in info_list if word != ""]
        print(info_list)

        tmp_cai = ""
        ping_flag = True
        kuan_flag = True
        for info in info_list:
            if "织" in info and len(info) < 4:
                res['织造方式'].append(info)
            if "%" in info:
                # res['材质'].append(info)
                tmp_cai += info
            if len(re.findall(r'[0-9]', info)) > 5 and "%" not in info and kuan_flag:
                res['款号'].append(info)
                kuan_flag = False
            if "无中文" in info and info.replace("无中文", "") != "":
                res['品牌'].append(info.replace("无中文", ""))
                ping_flag = False
        res['材质'].append(tmp_cai)
        # res['款号'].append(text_list_index_2[0].split("|")[1])
        # print(info_list[-2])
        res['品名'].append(info_list[0])
        if ping_flag:
            if info_list[-1].isdigit():
                res['品牌'].append(info_list[-2].replace("无中文", ""))
            else:
                res['品牌'].append(info_list[-1].replace("无中文", ""))
        res['原产国'].append(text_list_index_0[5])
        res['币制'].append(text_list_index_2[-1])
        tmp = text_list_index_2[-2]
        # print(1111, text_list_index_0[-5])
        # print(2222, text_list_index_1[-6])
        # print(3333, text_list_index_2[-2])

        num = ''.join(re.findall(r'[0-9]', tmp))
        res['数量'].append(num)
        res['单位'].append(tmp.replace(num, ""))
        res['总价'].append(text_list_index_1[-5])

        if kuan_flag:
            res["款号"].append("")
        # break

    # print(res)
    if "报关单号" not in res:
        res["报关单号"] = [""]
    info_length = len(res['项号'])
    for key in res:
        if len(res[key]) < info_length:
            res[key] += [""] * (info_length - len(res[key]))
        else:
            res[key] = res[key][:info_length]

    return res


def handle_something(tmp_list):
    flag_i = []
    for text_i in range(len(tmp_list)):
        if "|" in tmp_list[text_i] and "|" in tmp_list[text_i - 1]:
            tmp_list[text_i - 1] += "|"
            tmp_list[text_i - 1] += tmp_list[text_i]
            flag_i.append(text_i)
    if len(flag_i) > 0:
        for i in flag_i:
            tmp_list.pop(i)
    return tmp_list


def get_result(pdf_path):
    pdf = pdfplumber.open(pdf_path)
    all_result = list()
    # res = dict()
    page_index = 0
    for page in pdf.pages:
        res_page = one_page(page)
        res = dict()
        res["page"] = page_index
        res["result"] = res_page
        all_result.append(res)
        page_index += 1
        # break
    pdf.close()
    print(all_result)
    return all_result


# df = pd.DataFrame(res)
# print(df)
#
# df.to_csv(pdf_path.split("/")[-1].split(".")[0] + ".csv", index=None)
def get_excel(pdf_path):
    # writer = pd.ExcelWriter(pdf_path.split("/")[-1].split(".")[0] + ".xlsx")
    all_result = get_result(pdf_path)
    frames = []
    for index in range(len(all_result)):
        # print(index)
        # print(all_result[index])
        df = pd.DataFrame(all_result[index]['result'])
        frames.append(df)
        # df.to_excel(writer, sheet_name="Sheet" + str(index), index=False)
        # break
    result = pd.concat(frames)
    result = result[["报关单号", "项号", "款号", "商品编码", "品名", "品牌", "织造方式",
                     "材质", "原产国", "币制", "数量", "单位", "总价", "特殊关系确认",
                     "价格影响确认", "支付特许权使用费确认", "自报自缴"]]
    result.to_excel(pdf_path.split("/")[-1].split(".")[0] + ".xlsx", index=None)
    # writer.save()


if __name__ == '__main__':
    # get_result(pdf_path)
    import argparse

    parser = argparse.ArgumentParser(description="Params to use fro train algorithm")

    parser.add_argument("--pdf_path", "-pdf", type=str,
                        default="11.11/text.pdf", nargs='?', help="what scenes this model used")
    args = parser.parse_args()

    get_excel(args.pdf_path)
    # get_result(args.pdf_path)
