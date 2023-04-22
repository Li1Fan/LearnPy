# -*- coding: utf-8 -*-
import base64
import json
import string
from urllib.parse import quote

import requests
"""EMU登录"""
emu_ip = '192.168.222.133'
emu_port = 8081
name = 'test'
pwd = '809452ae6f9117b99cff17f977e3f2aa'

session = requests.Session()
session.headers = {
    "Referer": "http://{}:{}/admin/main.jsp".format(emu_ip, emu_port),
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Pragma": "no-cache",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Host": "{}:{}".format(emu_ip, emu_port),
    "Accept-Encoding": "gzip, deflate",
    "Cache-Control": "no-cache",
    "Authorization": ""
}

session.cookies.set('usename', name)
session.keep_alive = False
# 获取验证码图片
code_url = 'http://{}:{}/ems/base/image/code'.format(emu_ip, emu_port)
print(code_url)
res_code = session.get(code_url)
print(f'get code {res_code.status_code}')

a_1 = str(res_code.content, encoding="utf-8")
# print(f'text {a_1}')
a_1 = json.loads(a_1)
base64_file = a_1.get('content').get('imageCode')
base64_file = base64.urlsafe_b64decode(base64_file)
# 保存验证码图片
with open('/home/frz/fileTest/code', "wb") as f:
    f.write(base64_file)
    f.close()
vckey = a_1.get('content').get('verificationKey')
print(f'vckey:{vckey}')
# 手动识别
value = input()

# 登录，并处理数据
session.headers['Content-Type'] = 'application/json;charset=UTF-8'
data = {'username': name, 'password': pwd, 'verificationCode': value,
        'verificationKey': vckey}
# 数据转为json、字节类型
data = json.dumps(data)
post_data = bytes(data, 'utf8')
print(post_data)
res = session.post('http://192.168.222.133:8081/ems/base/login',
                   data=post_data, verify=False)  # 不做证书认证
print(res.status_code)
print(str(res.content, encoding='utf-8'))
