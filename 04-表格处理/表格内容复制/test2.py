import xlrd


def parse_excel(file_path):
    # 打开 Excel 文件
    workbook = xlrd.open_workbook(file_path)
    worksheet = workbook.sheet_by_index(0)

    # 创建一个空列表,用于存储每一行的数据
    data = []

    # 遍历工作表中的每一行
    for row_index in range(1, worksheet.nrows):
        # 提取每一行中需要的数据
        row_data = [
            worksheet.cell_value(row_index, 7),  # 编号
            worksheet.cell_value(row_index, 8),  # 经度
            worksheet.cell_value(row_index, 9),  # 纬度
            worksheet.cell_value(row_index, 10),  # 村名
            worksheet.cell_value(row_index, 4),  # 三调DLMC
            worksheet.cell_value(row_index, 3),  # 二普土壤类型
            worksheet.cell_value(row_index, 6),  # 二调DLMC
            worksheet.cell_value(row_index, 5),  # 三普土壤类型
            worksheet.cell_value(row_index, 11)  # 实际地类变化模式
        ]
        data.append(row_data)

    # 列表重新排序
    data.sort(key=lambda x: x[0].split('-')[-1])
    return data
