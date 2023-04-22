# -*- coding: utf-8 -*-
import re
from datetime import datetime, timedelta

import xlwt
from chinese_calendar import is_workday

MONTH_DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# current_time = datetime.now()
current_time = datetime(2022, 12, 1)

YEAR = current_time.year
MONTH = current_time.month
DAY = current_time.day


def str2time(str_):
    """将字符串转化为datetime，
    主要有三种类型：11-0108：50，星期五08：50，昨天08：50"""
    str_, ret = match_time(str_)
    if not str_:
        return None
    if ret == 1:
        return datetime(YEAR, int(str_[0:2]), int(str_[3:5]), int(str_[5:7]), int(str_[8:10]))
    if ret == 2:
        if '星期一' in str_:
            for n in range(7, 1, -1):
                if (current_time - timedelta(days=n)).isoweekday() == 1:
                    return datetime(YEAR, MONTH, DAY,
                                    int(str_[3:5]), int(str_[6:8])) - timedelta(days=n)
        if '星期二' in str_:
            for n in range(7, 1, -1):
                if (current_time - timedelta(days=n)).isoweekday() == 2:
                    return datetime(YEAR, MONTH, DAY,
                                    int(str_[3:5]), int(str_[6:8])) - timedelta(days=n)
        if '星期三' in str_:
            for n in range(7, 1, -1):
                if (current_time - timedelta(days=n)).isoweekday() == 3:
                    return datetime(YEAR, MONTH, DAY,
                                    int(str_[3:5]), int(str_[6:8])) - timedelta(days=n)
        if '星期四' in str_:
            for n in range(7, 1, -1):
                if (current_time - timedelta(days=n)).isoweekday() == 4:
                    return datetime(YEAR, MONTH, DAY,
                                    int(str_[3:5]), int(str_[6:8])) - timedelta(days=n)
        if '星期五' in str_:
            for n in range(7, 1, -1):
                if (current_time - timedelta(days=n)).isoweekday() == 5:
                    return datetime(YEAR, MONTH, DAY,
                                    int(str_[3:5]), int(str_[6:8])) - timedelta(days=n)
        if '星期六' in str_:
            for n in range(7, 1, -1):
                if (current_time - timedelta(days=n)).isoweekday() == 6:
                    return datetime(YEAR, MONTH, DAY,
                                    int(str_[3:5]), int(str_[6:8])) - timedelta(days=n)
        if '星期日' in str_:
            for n in range(7, 1, -1):
                if (current_time - timedelta(days=n)).isoweekday() == 7:
                    return datetime(YEAR, MONTH, DAY,
                                    int(str_[3:5]), int(str_[6:8])) - timedelta(days=n)
    if ret == 3:
        if '昨天' in str_:
            return datetime(YEAR, MONTH, DAY, int(str_[2:4]), int(str_[5:7])) - timedelta(days=1)
        elif '今天' in str_:
            return datetime(YEAR, MONTH, DAY, int(str_[2:4]), int(str_[5:7]))


def match_time(str_):
    """正则匹配字符串，
    三种类型：11-0108：50，星期五08：50，昨天08：50"""
    pattern_time = re.compile(r'^\d{2}-\d{4}:\d{2}$')
    pattern_week = re.compile(r'^星期[一二三四五六七日]\d{2}:\d{2}$')
    pattern_day = re.compile(r'^[昨今]天\d{2}:\d{2}$')
    if pattern_time.search(str_):
        return str_, 1
    elif pattern_week.search(str_):
        return str_, 2
    elif pattern_day.search(str_):
        return str_, 3
    else:
        return None, None


def week_of_the_month(sometime):
    """计算传入的日期属于该月的第几周"""
    year, month, day = sometime.year, sometime.month, sometime.day
    someday = datetime(year, month, 1)

    dayOfTheWeek = someday.isoweekday()
    sunday_date = 7 - dayOfTheWeek + 1
    month_day = MONTH_DAYS[month - 1]

    sunday_dates = [n * 7 + sunday_date for n in range(0, 5) if n * 7 + sunday_date <= month_day]
    sunday_dates.append(month_day)
    # print(sunday_dates)
    for n, _date in enumerate(sunday_dates):
        if _date >= day:
            return n + 1


def parse_data(data_list: list):
    """解析为datetime类型"""
    _lst = list()
    # 计算重复
    lst_repeat = list()
    for n, _date in enumerate(data_list):
        _t = str2time(_date.replace(' ', ''))
        if _t and _t.day not in lst_repeat:
            if _t > datetime(_t.year, _t.month, _t.day, 6, 0):
                _lst.append(_t)
                lst_repeat.append(_t.day)
    return _lst


def get_z_x(sometime):
    """获取第几周，星期几"""
    return week_of_the_month(sometime), sometime.isoweekday(),


def parse_ocr_result(str_):
    """切割数据"""
    return str_.strip().replace(' ', ''). \
        replace(': ', ':').replace('：', ':') \
        .replace('星期-', '星期一').split('\n')


def create_table(str_data):
    """创建表格"""
    data = parse_ocr_result(str_data)
    print(data)
    a = parse_data(data)
    print(a)
    print(f'打卡次数 {len(a)}')
    # 创建新的workbook（其实就是创建新的excel）
    workbook = xlwt.Workbook(encoding='ascii')
    # 创建新的sheet表
    worksheet = workbook.add_sheet("My new Sheet")
    # 往表格写入内容
    for i, v in enumerate(['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']):
        worksheet.write(0, i, v)

    # 写入颜色样式
    style = "font:colour_index red;"
    red_style = xlwt.easyxf(style)

    try:
        for i, date in enumerate(a):
            x, y = get_z_x(date)
            if is_workday(date) and \
                    date > datetime(date.year, date.month, date.day, 8, 52):
                worksheet.write(x, y - 1, str(date), style=red_style)
            else:
                worksheet.write(x, y - 1, str(date))
    except Exception as e:
        print(e)
        pass
    # 保存
    workbook.save("new.xls")


if __name__ == "__main__":
    # 从文件中读取数据
    with open('data.txt', 'r', encoding='utf-8') as f:
        data = f.read()
    create_table(data)
