import datetime
import json

import pymysql

# 打开数据库连接
from sql_db.robot.qv_robot_joke import getHTMLText, JOKE_API

db = pymysql.connect(host='localhost',
                     user='root',
                     password='qweasdzxc',
                     database='test')

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

cursor.execute('show tables;')
data = cursor.fetchall()
print(data)

cursor.execute('select * from joke')
result = cursor.fetchall()
print(result)
# a = '2010'
# b = '333'
# sql_cmd = 'insert into joke (id,time,con) values(1,"{}","{}")'.format(a, b)
# print(sql_cmd)

date = datetime.datetime.now().date()
print(date)
joke_json = getHTMLText(JOKE_API)
joke_str = json.loads(joke_json)
for i in range(10):
    message = joke_str.get('result')[i].get('content')
    # print(message)
    sql_cmd = 'insert into joke (id,time,con) values({},"{}","{}")'.format(i, date, message)
    cursor.execute(sql_cmd)

cursor.execute('select * from joke')
result = cursor.fetchall()
print(result)

cursor.close()

db.commit()
db.close()
