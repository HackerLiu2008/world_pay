import xlrd
from xlutils.copy import copy
from tools_me.mysql_tools import SqlData
import openpyxl


file_path = "C:\\Users\\Think\\Desktop\\截止11月13全球付手续费统计.xlsx"

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
money_list = col_list[7][1:]
cus_list = col_list[9][1:]

cus = list(set(cus_list))

index = 0
info_list = list()
for i in cus_list:
    indict = dict()
    indict[i] = money_list[index]
    info_list.append(indict)
    index += 1


for c in cus:
    res = 0
    for n in info_list:
        if c in n:
            res += float(n.get(c))
    print('客户名称: ' + c, ';   异常交易费累计: ', round(res, 2))



'''
index = 0
cus_list = list()
for card in card_list:
    if card:
        print(card)
        res = SqlData().search_card_info_admin("WHERE card_no = '" + card + "'")
        print(res)
        if res:
            cus_list.append(res[0].get('account_name'))
        else:
            card_list.append('')
    else:
        break

wb = openpyxl.load_workbook(file_path)
wb1 = wb.active
n = 2
for i in cus_list:
    wb1.cell(n, 10, i)
    n += 1
save_path = file_path
wb.save(save_path)
'''