import pymysql

# 打开数据库连接
db = pymysql.connect(host='localhost',
                     user='root',
                     password='qweasdzxc',
                     database='mydb')

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# sql = show tables;select * from student;select * from class;
# 使用 execute()  方法执行 SQL 查询
cursor.execute('show tables;')

# 使用 fetchone() 方法获取单条数据.
# data = cursor.fetchone()
data = cursor.fetchall()

print(data)

cursor.execute('select * from student')
result = cursor.fetchall()
print(result, type(result))

cursor.execute('select * from student where sid > 5')
result = cursor.fetchall()
print(result)
sql_cmd = 'update student set sname = "%s" where sid = %i' % ("miss", 7)
print(sql_cmd)
sql_cmd = 'update student set sname = "{}" where sid = {}'.format("miss", 7)
print(sql_cmd)
cursor.execute(sql_cmd)
cursor.execute('select * from student')
result = cursor.fetchall()
print(result)

# cursor.execute('select * from student where sid = 7')
# result = cursor.fetchall()
# print(result)

# cursor.execute('delete from user where id = ?', (2,))
# cursor.execute('select * from user')
# result = cursor.fetchall()
# print(result)

cursor.close()

db.commit()
# 关闭数据库连接
db.close()
