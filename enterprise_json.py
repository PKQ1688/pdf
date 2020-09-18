# -*- coding:utf-8 -*-
# @author :adolf
from collections import OrderedDict

right_name = ["企业名称", "统一社会信用代码", "工商注册号", "组织机构代码", "中征码", "经济类型", "组织机构类型", "企业规模", "所属行业",
              "成立年份", "登记证书有效截止日期", "登记地址", "办公/经营地址", "存续状态"]
last_name = ["首次有信贷交易的年份", "发生信贷交易的机构数", "当前有未结清信贷 交易的机构数", "首次有相关还款 责任的年份",
             "非信贷交易账户数", "欠税记录条数", "民事判决记录条数", "强制执行记录条数", "行政处罚记录条数"]
Enterprise_class_dict = OrderedDict()
Enterprise_class_dict["身份标识"] = ["身份标识"]
Enterprise_class_dict["异议提示"] = ["异议提示"]
Enterprise_class_dict["信息概要"] = ["信息概要提示", "未结清信贷及授信信息概要", "相关还款责任信息概要", "已结清信贷信息概要",
                                 "负债历史"]
Enterprise_class_dict["财务报表信息"] = ["附件2：财务报表信息"]
Enterprise_class_dict["信贷记录"] = ["（一）被追偿业务的历史表现"]
