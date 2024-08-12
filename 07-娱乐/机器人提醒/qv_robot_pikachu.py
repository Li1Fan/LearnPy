import base64
import hashlib
import re
import sys
import time

import requests
from bs4 import BeautifulSoup
import datetime
from chinese_calendar import is_workday

url = 'https://tianqi.moji.com/weather/china/fujian/minhou-county'
url_today = 'https://tianqi.moji.com/today/china/fujian/minhou-county'
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
}

ROBOT_HOOK = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=6d40e747-d1d4-445f-8d66-0d7ec52f5353"
TEST_ROBOT_HOOK = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=7486aec5-d41f-49b5-9605-1ffb24f5f186"
HEADERS = {
    "Content-Type": "text/plain"
}


# 获取天气预报
def get_weather_forecast():
    r = requests.get(url, headers=headers, timeout=30)
    r.encoding = r.apparent_encoding
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')

    # 贴士
    text_tips = soup.find_all(class_='wea_tips clearfix')
    re_tips = re.compile(r'<em>(.*?)</em>', re.S)
    result = re.findall(re_tips, str(text_tips))
    result_tip = result[0].replace('\n', '')

    # 地区
    result = re.findall(re_tips, str(html))
    result_location = result[0].split('，')[0].replace('\n', '')

    # 温度
    text_tem = soup.find_all(class_='days clearfix')
    re_tem = re.compile(r"<li>(\d+)° / (\d+)°</li>", re.S)
    result = re.findall(re_tem, str(text_tem[0]))
    result_tem = result[0][0], result[0][1]

    # 是否需要带伞
    text_umb = soup.find_all(class_='live_index_grid')
    if '不带伞' in str(text_umb):
        umbrella_flag = 0
    else:
        umbrella_flag = 1

    r_today = requests.get(url_today, headers=headers, timeout=30)
    r_today.encoding = r_today.apparent_encoding
    html_today = r_today.text
    soup = BeautifulSoup(html_today, 'html.parser')

    # 实时天气
    text_now = soup.find_all('div', class_='info clearfix')
    re_now = re.compile(r'<b>(.*?)</b>', re.S)
    result = re.findall(re_now, str(text_now[0]))
    result_now = result[0]

    # 天气转
    text_wea = soup.find_all('div', class_='day')
    re_wea = re.compile(r'<em>(.*?)</em>', re.S)
    result = re.findall(re_wea, str(text_wea[0]))
    result_wea1 = result[0]
    result = re.findall(re_wea, str(text_wea[1]))
    result_wea2 = result[0]
    if result_wea1 in result_wea2:
        result_wea = result_wea1
    else:
        result_wea = f'{result_wea1}转{result_wea2}'

    info = f'【天气提醒】\n' \
           f'{result_location}  {result_wea}  ' \
           f'{result_tem[0]}-{result_tem[1]}℃\n小贴士：{result_tip}'

    if umbrella_flag == 1:
        info = info + '记得带伞！'

    return info


# 发送文本信息
def send_message(message: str):
    send_data = {
        "msgtype": "text",
        "text": {
            "content": message,
            "mentioned_list": ["@all"]
        }
    }
    r = requests.post(url=ROBOT_HOOK, headers=HEADERS, json=send_data)
    return r


# 发送文本消息至个人小群
def send_message_test(message: str):
    send_data = {
        "msgtype": "text",
        "text": {
            "content": message,
            "mentioned_list": ["@all"]
        }
    }
    r = requests.post(url=TEST_ROBOT_HOOK, headers=HEADERS, json=send_data)
    return r


# 发送图片信息
def send_image_message(filename: str):
    send_data = {
        "msgtype": "image",
        "image": {
            "base64": base64_encode(filename),
            "md5": md5sum(filename)
        }
    }
    r = requests.post(url=ROBOT_HOOK, headers=HEADERS, json=send_data)
    return r


def transform_week(num):
    list_week = ['', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    return list_week[num]


def base64_encode(filename):
    with open(filename, 'rb') as f:
        encode_img = base64.b64encode(f.read())
        return encode_img


def md5sum(filename):
    with open(filename, 'rb') as f:
        contents = f.read()
        return hashlib.md5(contents).hexdigest()


if __name__ == "__main__":
    date = datetime.datetime.now().date()
    # date = datetime.date(2022, 3, 28)

    week = date.isoweekday()
    tomorrow = date + datetime.timedelta(days=1)
    yesterday = date - datetime.timedelta(days=1)

    if is_workday(date):
        info_date = '{} {}'.format(date, transform_week(week))
        info_weather = get_weather_forecast()
        send_message(info_weather)

        if is_workday(tomorrow) is False:
            send_message('下班下班，皮卡丘罢工啦！')
            time.sleep(0.5)
            try:
                send_image_message('/home/frz/PycharmProjects/PyLearn/service/robot/work_off.gif')
            except Exception as e:
                send_message_test('send image fail')
                send_message_test(str(sys.exc_info()[0]))
                send_message_test(str(e))

        if is_workday(yesterday) is False:
            send_message('悲催的打工丘，它回来了。')
            time.sleep(0.5)
            try:
                send_image_message('/home/frz/PycharmProjects/PyLearn/service/robot/work.gif')
            except Exception as e:
                send_message_test('send image fail')
                send_message_test(str(sys.exc_info()[0]))
                send_message_test(str(e))
    else:
        pass
