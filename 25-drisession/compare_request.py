url = 'https://baike.baidu.com/item/python'

# 使用 requests：
import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
response = requests.get(url, headers=headers)
html = etree.HTML(response.text)
# 找到第一个 h1 标签
element = html.xpath('//h1')[0]
title = element.text
print(title)
print(html.xpath('//h1/text()')[0])

# 使用 DrissionPage：
from DrissionPage import SessionPage

page = SessionPage()
page.get(url)
# 找到第一个 h1 标签
title = page('tag:h1').text
print(title)

url = 'https://www.baidu.com/img/flexible/logo/pc/result.png'
save_path = r'./'

# 使用 requests：
import requests

r = requests.get(url)
with open(f'{save_path}/img.png', 'wb') as fd:
    # 分块写入文件
    for chunk in r.iter_content():
        fd.write(chunk)
    # 或者直接写入
    # fd.write(r.content)

# 使用 DrissionPage：
from DrissionPage import SessionPage

page = SessionPage()
page.download(url, save_path, 'img')  # 支持重命名，处理文件名冲突
