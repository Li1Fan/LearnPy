import requests

ROBOT_HOOK = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=6d40e747-d1d4-445f-8d66-0d7ec52f5353"
HEADERS = {
    "Content-Type": "text/plain"
}


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


send_message('123')
