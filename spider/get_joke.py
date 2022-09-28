import json
import re


import requests
from lxml import etree


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


def parse_html(html):
    e = etree.HTML(html)
    urls = e.xpath("//div[@class='col1 old-style-col1']/div/a[1]/@href")
    url = ["https://www.qiushibaike.com{}".format(url) for url in urls]
    for i in url:
        print(i)
        data = get_html(i)
        title = re.findall(r"<h1>(.*?)</h1>", data, re.S)[0]
        title = title.strip()
        tata = re.findall(r'<div class="content">(.*?)</div>', data, re.M)[0]
        tata = tata.replace("<br/>", "").strip()
        with open("json.json", 'a+', encoding="utf-8") as f:
            dict = {"标题": title, "笑话": tata}
            f.write(json.dumps(dict, ensure_ascii=False))
            f.write("\n")


if __name__ == '__main__':
    # 翻页获取
    for i in range(2):
        url = "https://www.qiushibaike.com/text/page/{}".format(i)
        html = get_html(url)
        parse_html(html)
        print(1)
