# -*- coding:utf-8 -*-
# @author :adolf
last_row_key_list = ['被查询者姓名', '异议信息提示', '性别', '学历', '通讯地址', '数字解读', '相对位置']
mul_row_key_list = ['说明', '账户类型', '业务大类', '业务类型', '账户数', '首笔业务发放月份']

First_Class_match = {
    '基础': {
        '基础信息': ['报告编号', '报告时间', '被查询者姓名', '被查询者证件类型', '被查询者证件号码', '查询机构', '查询原因',
                 '异议信息提示']},
    '个人基本信息': {
        '身份信息': ['性别', '出生日期', '婚姻状况', '就业状况', '学历', '学位', '国籍', '电子邮箱', '通讯地址', '户籍地址',
                 '手机号码', '信息更新日期'],
        '配偶信息': ['姓名', '证件类型', '证件号码', '工作单位', '联系电话'],
        '居住信息': ['居住地址', '住宅电话', '居住状况', '信息更新日期'],
        '职业信息': ['工作单位', '单位性质', '单位地址', '单位地址', '职业', '行业', '职务', '职称', '进入本单位年份',
                 '信息更新日期']},
    '信息概要': {
        '个人信用报告“数字解读”': ['数字解读', '相对位置', '说明'],
        '信贷交易信息提示': ['账户类型', '账户数', '月份数', '单月最高逾期/透支总额', '最长逾期/透支月数'],
        '信贷交易违约信息概要': ['管理机构数', '账户数', '授信总额', '余额', '最近6个月平均应还款'],
        '信贷交易授信及负债信息概要': [],
        '非信贷交易信息概要': [],
        '公共信息概要': [],
        '查询记录概要': []
    }
}
