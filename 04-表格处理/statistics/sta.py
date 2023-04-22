import calendar
import os
import xlwt


class Statistics:

    def __init__(self):
        self.items = dict()
        self.total_data = dict()

    def handle_text(self, value_list: list, type):
        year = int(value_list[1][4])
        month = int(value_list[1][5])
        staionId_list = self.get_stationId(value_list)
        for value in value_list:
            if 'Year' in value:
                continue
            stationId = value[0]
            value1 = value[7]  # 20-8时降水量（夜晚） 求平均
            value2 = value[8]  # 8-20时降水量(白天)   求平均
            value3 = value[9]  # 20-20时累计降水量    求和
            if stationId + '-value1' not in self.items.keys():
                self.items.update({stationId + '-value1': []})
                self.items.update({stationId + '-value2': []})
                self.items.update({stationId + '-value3': []})
            self.items[stationId + '-value1'].append(int(value1))
            self.items[stationId + '-value2'].append(int(value2))
            self.items[stationId + '-value3'].append(int(value3))
        days = calendar.monthrange(year, month)
        for stationId in staionId_list:
            v1_list = self.items[stationId + '-value1']
            v2_list = self.items[stationId + '-value2']
            v3_list = self.items[stationId + '-value3']
            # 处理数据
            if type == 1:
                last_value1 = sum(v1_list) / days[1]
                last_value2 = sum(v2_list) / days[1]
                last_value3 = sum(v3_list)
            else:
                last_value1 = sum(v1_list) / days[1] * 0.1
                last_value2 = sum(v2_list) / days[1] * 0.1
                last_value3 = sum(v3_list) / days[1] * 0.1
            # result = sum(v1_list) / days[1], sum(v2_list) / days[1], sum(v3_list)
            # 数据格式 {stationId：([v1,],[v2,],[v3],[year])}
            if stationId not in self.total_data.keys():
                self.total_data.update({stationId: ([], [], [], [])})
            self.total_data[stationId][0].append(last_value1)
            self.total_data[stationId][1].append(last_value2)
            self.total_data[stationId][2].append(last_value3)
            if year not in self.total_data[stationId][3]:
                self.total_data[stationId][3].append(year)
        self.items = dict()

    def get_stationId(self, value_list: list):
        lst = list()
        for value in value_list:
            if 'Year' in value:
                continue
            if value[0] not in lst:
                lst.append(value[0])
        return lst


def read_file(file_path):
    with open(file_path) as f:
        text_list = f.readlines()
    split_list = list()
    for text in text_list:
        # 切割字符
        if '\t' in text:
            text_split = text.split('\t')
        else:
            text_split = text.split(' ')
            text_split = list(filter(None, text_split))
        split_list.append(text_split)
    return split_list


def get_files(dir, year):
    lst = list()
    for root, dirs, files in os.walk(dir):
        if root == dir:
            for name in files:
                if year == name[3:7]:
                    lst.append(os.path.join(root, name))
    return lst


def create_table(data, type):
    # 创建新的workbook（其实就是创建新的excel）
    workbook = xlwt.Workbook(encoding='ascii')

    def write_table(key, type):
        if type == 1:
            name = {1: "月夜晚平均", 2: "月白天平均", 3: "月累积"}[key]
        else:
            name = {1: "平均气温", 2: "最高气温", 3: "最低气温"}[key]
        # 创建新的sheet表
        worksheet = workbook.add_sheet(name)

        # 往表格写入内容
        # worksheet.write(0, 0, "内容1")
        # worksheet.write(2, 1, "内容2")
        worksheet.write(0, 0, "站点")
        for i in range(12):
            worksheet.write(0, i + 1, str(i + 1) + '月')
        for i, stationId in enumerate(sorted(list(data.keys()))):
            v1 = data[stationId][key - 1]
            worksheet.write(i + 1, 0, stationId)
            for j, value in enumerate(v1):
                worksheet.write(i + 1, j + 1, value)

    write_table(1, type)
    write_table(2, type)
    write_table(3, type)

    # 保存
    if type == 1:
        workbook.save('降水' + year + ".xls")
    else:
        workbook.save('气温' + year + ".xls")


if __name__ == "__main__":
    path = r'E:\WeChat Files\wxid_hqdtktnqvw8e21\FileStorage\File\2023-02\TEM'
    year = '2015'
    # 1代表降水 2代表气温
    type = 2
    s = Statistics()
    files = get_files(path, year)
    for file in files:
        data = read_file(file)
        s.handle_text(data, type)
    print(s.total_data)
    create_table(s.total_data, type)
