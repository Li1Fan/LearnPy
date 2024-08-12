# coding:utf-8
import re

import xlwt

text = '玉辉：111永宝：123'
# print(text.split())
# pattern = re.compile(r'\d+')
# m = pattern.match(text)
# print(m)
pattern = re.compile(r'\d+')
list_number = pattern.findall(text)
print(list_number)
# TODO：正则要好好重新学一遍
pattern_name = re.compile(r'([^\d^：]*)：')
list_name = pattern_name.findall(text)
print(list_name, '\n', len(list_name))
text = text.replace('0', '')
text = text.replace('1', '')
text = text.replace('2', '')
text = text.replace('3', '')
text = text.replace('4', '')
text = text.replace('5', '')
text = text.replace('6', '')
text = text.replace('7', '')
text = text.replace('8', '')
text = text.replace('9', '')
text = text.replace('0', '')
list_name = text.split('：')
print(list_name)

# 创建新的workbook（其实就是创建新的excel）
workbook = xlwt.Workbook(encoding='ascii')

# 创建新的sheet表
print(len(list_number))
print(len(list_name))

worksheet = workbook.add_sheet("My new Sheet")

# 往表格写入内容
# worksheet.write(0, 0, "内容1")
# worksheet.write(2, 1, "内容2")
try:
    for i, name in enumerate(list_name):
        worksheet.write(i, 0, name)
        worksheet.write(i, 1, list_number[i])
except:
    pass
# 保存
workbook.save("new.xls")
