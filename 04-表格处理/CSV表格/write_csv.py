# -*- coding: utf-8 -*-
import csv

# header = ['name', 'age', 'qq', 'vx']
#
# data = [['xh', '21', '787991021', 'xh787991021'], ['xm', '21', '787991022', 'xm787991022']]
# with open('information.csv', 'w', encoding='utf-8', newline='') as fp:
#     # 写
#     writer = csv.writer(fp)
#     # 设置第一行标题头
#     writer.writerow(header)
#     # 将数据写入
#     writer.writerows(data)

print("*" * 30)
# 字典

header = ['name', 'age']

data = [{'name': 'suliang', 'age': '21'},
        {'name': 'xiaoming', 'age': '22'},
        {'name': 'xiaohu', 'age': '25'}]
with open('information.csv', 'w', encoding='utf-8', newline='') as fp:
    # 写
    writer = csv.DictWriter(fp, header)
    # 写入标题
    writer.writeheader()
    # 将数据写入
    writer.writerows(data)
