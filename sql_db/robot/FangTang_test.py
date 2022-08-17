# coding=utf-8
import re

import requests
import traceback

# from qv_robot_pikachu import get_weather_forecast
from bs4 import BeautifulSoup

# KEY = 'SCT155574TuMU7IV2zqWikQufVeNFNFhPC'
# KEY = 'SCT155642TIvMHD1VJwGd1hJDjJeOYTmL9'

url = 'https://tianqi.moji.com/weather/china/fujian/cangshan-district'
url_today = 'https://tianqi.moji.com/today/china/fujian/cangshan-district'
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
}


# 获取天气预报
def get_weather_forecast():
    r = requests.get(url, headers=headers, timeout=30)
    r.encoding = r.apparent_encoding
    html = r.text
    if '403' in html:
        return
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


def msg_push(KEY, title, content):
    try:
        url = 'https://sctapi.ftqq.com/%s.send' % KEY
        requests.post(url, data={'text': title, 'desp': content})
    except Exception as e:
        traceback.format_exc()
        print(e)


if __name__ == '__main__':
    info_weather = get_weather_forecast()
    lst_weather = info_weather.split('\n')

    title = lst_weather[1].replace('  ', ' ')
    if '伞' in info_weather:
        title += ' ☂'
    content = info_weather.replace('\n', '\n\n')
    # print(title, '\n', content)

    KEY1 = 'SCT155574TuMU7IV2zqWikQufVeNFNFhPC'
    msg_push(KEY1, title, content)
    KEY2 = 'SCT155642TIvMHD1VJwGd1hJDjJeOYTmL9'
    msg_push(KEY2, title, content)
