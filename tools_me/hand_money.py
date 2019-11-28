from os import path

import xlrd
from openpyxl.drawing.image import Image
from xlutils.copy import copy
from tools_me.mysql_tools import SqlData
import openpyxl
import os

print(os.path.abspath(''))

file_path = "C:\\Users\\Think\\Desktop\\world_pay_demo.xls"


data = xlrd.open_workbook(file_path, encoding_override='utf-8')
table = data.sheets()[0]
nrows = table.nrows  # 行数
ncols = table.ncols  # 列数
# row_list = list()
# method = 'c'
# if method == 'r':
row_list = [table.row_values(i) for i in range(0, nrows)]  # 所有行的数据
print(row_list)
# elif method == 'c':
col_list = [table.col_values(i) for i in range(0, ncols)]  # 所有列的数据
card_list = col_list[0][1:]

for i in card_list:
    print(i.strip())

for i in col_list[1]:
    print(i)


'''
wb = openpyxl.load_workbook(file_path)
wb1 = wb.active
img_path = "G:\\world_pay\\static\\pay_pic\\大龙_20191107101121e40ed.png"
img = Image(img_path)
img.width = 400
img.height = 400
wb1.add_image(img, 'K1')
save_path = file_path
wb.save(save_path)
'''
