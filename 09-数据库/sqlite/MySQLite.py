import sqlite3
from collections import OrderedDict


class MySQLite:
    def __init__(self, db_path):
        """
        初始化数据库连接和游标对象

        :param db_path: 数据库文件路径
        """
        self.db_path = db_path

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cur = self.conn.cursor()

    def execute(self, sql, args=()):
        """
        执行 SQL 语句

        :param sql: SQL 语句
        :param args: SQL 语句中的参数，可选
        :return: 执行成功返回 True，执行失败返回 False
        """
        print(f'CMD sql:{sql}, args:{args}')
        self.connect()
        try:
            self.cur.execute(sql, args)
            self.conn.commit()
            ret = True
        except Exception as e:
            print(f'CMD error: {e}')
            self.conn.rollback()
            ret = False
        self.close()
        return ret

    def insert(self, table, data):
        """
        插入数据

        :param table: 表名
        :param data: 字典形式的数据，键为列名，值为要插入的数据
        :return: 执行成功返回 True，执行失败返回 False
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join('?' * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        return self.execute(sql, tuple(data.values()))

    def delete(self, table, where):
        """
        删除数据

        :param table: 表名
        :param where: 删除数据的条件语句
        :return: 执行成功返回 True，执行失败返回 False
        """
        sql = f"DELETE FROM {table} WHERE {where}"
        return self.execute(sql)

    def update(self, table, data, where):
        """
        更新数据

        :param table: 表名
        :param data: 字典形式的数据，键为列名，值为要更新的数据
        :param where: 更新数据的条件语句
        :return: 执行成功返回 True，执行失败返回 False
        """
        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {where}"
        return self.execute(sql, tuple(data.values()))

    def select(self, table, columns='*', where=None):
        """
        查询数据

        :param table: 表名
        :param columns: 要查询的列名，用逗号分隔，默认为所有列
        :param where: 查询数据的条件语句
        :return: 返回查询到的数据
        """
        sql = f"SELECT {columns} FROM {table}"
        if where:
            sql += f" WHERE {where}"
        print(f'CMD sql:{sql}')
        self.connect()
        try:
            self.cur.execute(sql)
            ret = self.cur.fetchall()
        except Exception as e:
            print(f'CMD error:{e}')
            ret = None
        self.close()
        return ret

    def close(self):
        """
        关闭数据库连接和游标对象
        """
        self.cur.close()
        self.conn.close()

    def create_table(self, table_name, columns):
        """
        创建表格

        :param table_name: 表格名称
        :param columns: 字典形式的表格列名和数据类型，键为列名，值为数据类型、数据属性
        """
        column_lst = []
        for column_name, column_type in columns.items():
            column_def = f"{column_name} {column_type}"
            column_lst.append(column_def)

        column_lst_str = ", ".join(column_lst)
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_lst_str})"
        self.execute(sql)

    def drop_table(self, table):
        """
        删除表格

        :param table: 要删除的表格名称
        """
        sql = f"DROP TABLE IF EXISTS {table}"
        return self.execute(sql)

    def get_all_tables(self):
        """
        获取数据库中所有表格的名称

        :return: 所有表格的名称组成的列表
        """
        self.connect()
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cur.fetchall()
        self.close()
        return [table[0] for table in tables]


if __name__ == "__main__":
    db = MySQLite('example.db')

    # 新增表格
    # 单列约束
    columns = OrderedDict({'id': 'integer primary key autoincrement not null',
                           'name': 'text not null unique',
                           'age': 'integer not null'})
    db.create_table('students', columns)
    # 组合结束
    # columns = OrderedDict({'id': 'integer primary key autoincrement not null',
    #                        'name': 'text not null',
    #                        'age': 'integer not null',
    #                        'UNIQUE': ('name', 'age')})
    # db.create_table('students', columns)

    # # 删除表格
    # db.drop_table('students')

    # 插入一条数据
    data = {'name': 'Tom', 'age': 18}
    db.insert('students', data)

    # 查询数据
    result = db.select('students', where="")
    print(result)

    # 更新一条数据
    data = {'age': 19}
    where = "name = 'Tom'"
    db.update('students', data, where)

    # 查询数据
    result = db.select('students', where="")
    print(result)

    # 删除一条数据
    where = "name = 'Tom'"
    db.delete('students', where)

    # 查询数据
    result = db.select('students', where="")
    print(result)

    # 获取所有表格
    r = db.get_all_tables()
    print(r)
