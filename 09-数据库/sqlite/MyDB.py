from collections import OrderedDict
from MySQLite import MySQLite


class MyDB:
    def __init__(self, db_pth):
        self.db = MySQLite(db_pth)

    def init_data(self):
        self.create_DevInfo_table()
        self.create_GroupInfo_table()
        self.create_Dev4Group_table()
        self.create_AlarmInfo_table()

    def create_DevInfo_table(self):
        columns = OrderedDict({'dev_id': 'integer primary key autoincrement not null',
                               'sn': 'text not null unique',
                               'mac': 'text not null',
                               'dev_type': 'text not null',
                               'sw_ver': 'text not null',
                               'hw_ver': 'text not null'})
        return self.db.create_table('DevInfo', columns)

    def create_GroupInfo_table(self):
        columns = OrderedDict({'group_id': 'integer primary key autoincrement not null',
                               'name': 'text not null unique'})
        return self.db.create_table('GroupInfo', columns)

    def create_Dev4Group_table(self):
        columns = OrderedDict({'dev4group_id': 'integer primary key autoincrement not null',
                               'dev_id': 'integer not null',
                               'group_id': 'integer not null',
                               'UNIQUE': ('dev_id', 'group_id')})
        return self.db.create_table('Dev4Group', columns)

    def create_AlarmInfo_table(self):
        columns = OrderedDict({'alarm_id': 'integer primary key autoincrement not null',
                               'dev_id': 'integer not null',
                               'alarm_type': 'text not null',
                               'alarm_time': 'text not null',
                               'alarm_status': 'text not null'})
        return self.db.create_table('AlarmInfo', columns)

    def insert_DevInfo_table(self, data):
        return self.db.insert('DevInfo', data)

    def insert_GroupInfo_table(self, data):
        return self.db.insert('GroupInfo', data)

    def insert_Dev4Group_table(self, data):
        return self.db.insert('Dev4Group', data)

    def insert_AlarmInfo_table(self, data):
        return self.db.insert('AlarmInfo', data)

    def delete_DevInfo_table(self, where):
        return self.db.delete('DevInfo', where)

    def delete_GroupInfo_table(self, where):
        return self.db.delete('GroupInfo', where)

    def delete_Dev4Group_table(self, where):
        return self.db.delete('Dev4Group', where)

    def delete_AlarmInfo_table(self, where):
        return self.db.delete('AlarmInfo', where)

    def update_DevInfo_table(self, data, where):
        return self.db.update('DevInfo', data, where)

    def update_GroupInfo_table(self, data, where):
        return self.db.update('GroupInfo', data, where)

    def update_Dev4Group_table(self, data, where):
        return self.db.update('Dev4Group', data, where)

    def update_AlarmInfo_table(self, data, where):
        return self.db.update('AlarmInfo', data, where)

    def select_DevInfo_table(self, columns='*', where=None):
        return self.db.select('DevInfo', columns, where)

    def select_GroupInfo_table(self, columns='*', where=None):
        return self.db.select('GroupInfo', columns, where)

    def select_Dev4Group_table(self, columns='*', where=None):
        return self.db.select('Dev4Group', columns, where)

    def select_AlarmInfo_table(self, columns='*', where=None):
        return self.db.select('AlarmInfo', columns, where)

    def insert_Dev4Group_table_by_sn_name(self, sn_name, group_name):
        dev_id = d.select_DevInfo_table(columns='dev_id', where=f'sn="{sn_name}"')[0][0]
        group_id = d.select_GroupInfo_table(columns='group_id', where=f'name="{group_name}"')[0][0]
        return self.insert_Dev4Group_table({'dev_id': dev_id, 'group_id': group_id})


if __name__ == "__main__":
    d = MyDB('Dev.db')

    d.init_data()
    print(d.db.get_all_tables())

    dev_info = {'sn': 'R13453453534', 'mac': 'JKJK2342KLKLJL',
                'dev_type': 'DP32G', 'sw_ver': 'V1.0', 'hw_ver': 'V2.0'}
    d.insert_DevInfo_table(dev_info)
    group_info = {'name': '测试一部'}
    d.insert_GroupInfo_table(group_info)

    sn_name = 'R13453453534'
    group_name = '测试一部'

    # dev_id = d.select_DevInfo_table(columns='dev_id', where=f'sn="{sn_name}"')[0][0]
    # group_id = d.select_GroupInfo_table(columns='group_id', where=f'name="{group_name}"')[0][0]
    # print(dev_id)
    # print(group_id)
    # d.insert_Dev4Group_table({'dev_id': dev_id, 'group_id': group_id})

    d.insert_Dev4Group_table_by_sn_name(sn_name, group_name)

    print(d.select_DevInfo_table())
    print(d.select_GroupInfo_table())
    print(d.select_Dev4Group_table())

    # d.db.cur.execute("PRAGMA table_info(DevInfo)")
    # print(d.db.cur.fetchall())
