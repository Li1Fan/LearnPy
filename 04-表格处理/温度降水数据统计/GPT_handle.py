import os
import xlrd
import xlwt


def get_files(dir):
    lst = list()
    for root, dirs, files in os.walk(dir):
        if root == dir:
            for name in files:
                if name[-3:] == ('xls') and len(name) == 11:
                    lst.append(os.path.join(root, name))
    return lst


def handle(file, dir, multiple):
    # 打开 Excel 文件
    input_workbook = xlrd.open_workbook(file)
    # input_worksheet = input_workbook.sheet_by_index(0)

    # 创建一个新的 Excel 文件对象
    output_workbook = xlwt.Workbook(encoding='utf-8')
    # output_worksheet = output_workbook.add_sheet('Sheet1')

    for i in range(3):
        input_worksheet = input_workbook.sheet_by_index(i)
        name = os.path.basename(file)
        # 降水
        if 'PRE' in name:
            output_worksheet = output_workbook.add_sheet(['月夜晚平均', '月白天平均', '月累积'][i],
                                                         cell_overwrite_ok=True)
            change_sheet_index = 2
        # 气温
        else:
            output_worksheet = output_workbook.add_sheet(['平均气温', '最高气温', '最低气温'][i],
                                                         cell_overwrite_ok=True)
            change_sheet_index = 0
        # 处理数据并写入工作表
        for row_index in range(input_worksheet.nrows):
            for col_index in range(input_worksheet.ncols):
                value = input_worksheet.cell_value(row_index, col_index)
                if row_index == 0 or col_index == 0:
                    # 如果是第一行以及第一列，跳过
                    new_value = value
                else:
                    new_value = value * multiple
                output_worksheet.write(row_index, col_index, new_value)
            # 降水
            if change_sheet_index == 2 and i == change_sheet_index:
                if row_index == 0:
                    output_worksheet.write(row_index, input_worksheet.ncols, '1-3月累积')
                else:
                    output_worksheet.write(row_index, input_worksheet.ncols, label=xlwt.Formula('SUM(B{}:D{})'.
                                                                                                format(row_index + 1,
                                                                                                       row_index + 1)))
            # 气温
            if change_sheet_index == 0 and i == change_sheet_index:
                if row_index == 0:
                    output_worksheet.write(row_index, input_worksheet.ncols, '1-3月平均气温')
                else:
                    output_worksheet.write(row_index, input_worksheet.ncols, label=xlwt.Formula('AVERAGE(B{}:D{})'.
                                                                                                format(row_index + 1,
                                                                                                       row_index + 1)))

    # 保存 Excel 文件
    # dir = os.path.dirname(file)
    name = os.path.basename(file)
    name = name.split('.')[0]
    output_workbook.save(dir + '/' + name + '-new.xls')


if __name__ == "__main__":
    # 传入源文件夹路径
    path = r'C:\Users\10262\Desktop\1'
    # 生成文件夹路径
    purpose_path = r"C:\Users\10262\Desktop\1"
    # 倍数关系
    multi = 0.1
    files = get_files(path)
    for file in files:
        try:
            handle(file, purpose_path, multi)
        except Exception as e:
            print(f'异常文件：{file}')
            print(e)
