# encoding:utf-8

import requests
import base64

"""
获取 Access Token
"""

API_KEY = 'saGr3AYcZ06LWa8E0GORrlj7'
SECRET_KEY = 'sbm6Xoa3P8KxQumOYZvNFacKaOBhKTMR'

# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'. \
    format(API_KEY, SECRET_KEY)
response = requests.get(host)
# if response:
#     print(response.json())
access_token = response.json()['access_token']

'''
通用文字识别（高精度版）
'''

request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
# 二进制方式打开图片文件
f = open('code.png', 'rb')
img = base64.b64encode(f.read())

params = {"image": img}
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    print(response.json())
