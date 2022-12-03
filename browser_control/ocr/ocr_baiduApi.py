# encoding:utf-8

import requests
import base64

"""
获取 Access Token
"""

API_KEY = 'saGr3AYcZ06LWa8E0GORrlj7'
SECRET_KEY = 'sbm6Xoa3P8KxQumOYZvNFacKaOBhKTMR'


def get_baiduApi_token():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'. \
        format(API_KEY, SECRET_KEY)
    response = requests.get(host)
    if response:
        access_token = response.json()['access_token']
        print(access_token)
        return access_token


def baiduApi_ocr(path):
    '''
    通用文字识别（高精度版）
    '''
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    # request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    # 二进制方式打开图片文件
    f = open(path, 'rb')
    img = base64.b64encode(f.read())

    params = {"image": img}
    request_url = request_url + "?access_token=" + get_baiduApi_token()
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        result = response.json()['words_result']
        return result


if __name__ == "__main__":
    print(baiduApi_ocr(r'C:\Users\10262\Downloads\Compressed\2022111222734490\2022111222734490da_1_0.jpg'))
