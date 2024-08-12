# -*- coding: utf-8 -*-
import csv

# 列表
with open('information.csv', encoding='utf-8')as fp:
    reader = csv.reader(fp)
    # 获取标题
    header = next(reader)  # ?!
    print(header)
    # 遍历数据
    dic = dict()
    for i in reader:
        print(i)
        dic.update({str(i[0]): i})
    print(dic)

print('*'*20)
# 字典
with open('information.csv', encoding='utf-8')as fp:
    reader = csv.DictReader(fp)
    for i in reader:
        print(i)
