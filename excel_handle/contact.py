# coding:utf-8
import re

import xlrd
import xlwt

text = '玉辉：13713180648永宝：18876368352炳坤：13599733405全土：13559418154伟鹏：13799496607永远：15059685521树枝：13799207083鑫涛：13859737493杰怀：13645948926志培：15259291798新民：13615960553培裕：18505077321财勇：13960220875新国：13636936926吉水：13400836062福顺：13706088423建兴：13859733010碧兰：13459526829明吉：15750705853财木：15968749668端平：18179522152财山：13859735479土金：15396442198财忠：13380165866文发：15559514262庆泉：15859483854明德：13024845874振丁：15059578139铭进：13666089835永顺：13602394698两旺：13636936774溪山：18950119810茂丁：15959617264鹏坚：15280276869锦明：13959937413春明：15159804181文强：13459259364鹏森：18859669709玉水：15759801745金和：13675934707荣贵：13829165109景林：15985889663顺龙：13489782046金坤：18859437660荣富：13959938303锋艺：15959529294'
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
print(list_name,'\nhhhh',len(list_name))
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
# for i, j in enumerate(list_number):
#     if len(j) != 11:
#         print(i, j)
# wb = xlrd.open_workbook('C:/Users/10262/Desktop/contacts.xlsx', encoding_override="utf-8")
# diff_sheet = wb.sheet_by_index(0)
# for i in range(1, diff_sheet.nrows):
#     """
#     0: empty 1: string 2: float 3: date 4: boolean 5: error
#     """
#     for j in range(diff_sheet.ncols):
#         cell_value = diff_sheet.row_values(i)[j]
#         print(cell_value)

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
