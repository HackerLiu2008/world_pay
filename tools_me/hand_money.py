import xlrd
from xlutils.copy import copy
from tools_me.mysql_tools import SqlData
import openpyxl


file_path = "C:\\Users\\Think\\Desktop\\helen最新客户免费开卡量.xlsx"

data = xlrd.open_workbook(file_path, encoding_override='utf-8')
table = data.sheets()[0]
nrows = table.nrows  # 行数
ncols = table.ncols  # 列数
row_list = list()
# method = 'c'
# if method == 'r':
#     row_list = [table.row_values(i) for i in range(0, nrows)]  # 所有行的数据
# elif method == 'c':
col_list = [table.col_values(i) for i in range(0, ncols)]  # 所有列的数据
card_list = col_list[0][1:]
pay_money = col_list[4][1:]

index = 0
info_list = list()
for i in card_list:
    indict = dict()
    indict[i] = pay_money[index]
    info_list.append(indict)
    index += 1

print(info_list)
for i in info_list:
    cus_name = list(i.keys())[0]
    free = int(i.get(cus_name))
    # print(free)
    if free<1:
        print(i)
    else:
        res = SqlData().search_user_field_name('account', cus_name)
        SqlData().update_account_field('free', free, cus_name)

'''
index = 0
cus_list = list()
for card in card_list:
    print(card)
    res = SqlData().search_card_info_admin("WHERE card_no = '" + card + "'")
    if res:
        cus_list.append(res[0].get('account_name'))
    else:
        card_list.apped('')



wb = openpyxl.load_workbook(file_path)
wb1 = wb.active
n = 2
for i in cus_list:
    wb1.cell(n, 12, i)
    n += 1
save_path = "C:\\Users\\Think\\Desktop\\统计后的客户.xlsx"
wb.save(save_path)
'''