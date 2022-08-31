import json
from collections import OrderedDict

import xlrd
import xlwt

dict_ = OrderedDict()
list_=list()
wb = xlrd.open_workbook('C:/Users/10262/Desktop/通用.xlsx', encoding_override="utf-8")
diff_sheet = wb.sheet_by_index(0)
for i in range(1, diff_sheet.nrows):
    """
    0: empty 1: string 2: float 3: date 4: boolean 5: error
    """
    # for j in range(diff_sheet.ncols):
    #     cell_value = diff_sheet.row_values(i)[j]
    #     print(cell_value)
    cell_value = diff_sheet.row_values(i)[0]
    list_.append(cell_value)
    cell_value_2 = diff_sheet.row_values(i)[1]

    dict_[cell_value] = cell_value_2
print(list_)
print(dict_)
# json.dump(dict_, open('data.json', 'w', encoding='utf-8'), ensure_ascii=False, sort_keys=False)

# 创建新的workbook（其实就是创建新的excel）
workbook = xlwt.Workbook(encoding='ascii')

# 创建新的sheet表
worksheet = workbook.add_sheet("My new Sheet")

# 往表格写入内容
# worksheet.write(0, 0, "内容1")
# worksheet.write(2, 1, "内容2")
try:
    for i, name in enumerate(list_):
        worksheet.write(0, i, name)
except:
    pass
# 保存
workbook.save("json.xls")