import datetime
import json

import requests
from chinese_calendar import is_workday

JOKE_API = 'http://v.juhe.cn/joke/randJoke.php?key=b522bfca8153cbcdb7330bcce80b63ca'
TEST_ROBOT_HOOK = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=7486aec5-d41f-49b5-9605-1ffb24f5f186"
HEADERS = {
    "Content-Type": "text/plain"
}
# ROBOT_HOOK = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=6d40e747-d1d4-445f-8d66-0d7ec52f5353"


def send_message(message: str):
    send_data = {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }
    r = requests.post(url=TEST_ROBOT_HOOK, headers=HEADERS, json=send_data)
    return r


def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        # r.raise_for_status()  # 如果状态不是200，引发HTTPError异常#
        r.encoding = r.apparent_encoding
        return r.text
    except Exception as e:
        return e


if __name__ == "__main__":
    date = datetime.datetime.now().date()
    if is_workday(date):
        joke_json = getHTMLText(JOKE_API)
        joke_str = json.loads(joke_json)
        # print(joke_str)
        # send_message('轻松一下')
        for i in range(3):
            message = joke_str.get('result')[i].get('content')
            # print(message)
            # print(''.join(message.split()))
            # send_message(message)
            send_message(''.join(message.split()))
