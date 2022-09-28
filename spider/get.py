import requests


def get_html(url):
    # 进行头部伪装，让浏览器认为是浏览器访问
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
    }
    res = requests.get(url, headers=headers)
    res.encoding = "utf-8"
    if res.status_code == 200:
        return res.text
    else:
        return None


if __name__ == "__main__":
    print(get_html('http://www.baidu.com'))
