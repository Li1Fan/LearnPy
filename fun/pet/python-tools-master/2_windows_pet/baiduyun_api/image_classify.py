# encoding:utf-8

import requests
import os
import base64
import time

"""
获取 Access Token
"""
API_KEY = 'xBPmKUlzLiRubiTRB2DAGYiC'
SECRET_KEY = 'OpMgnerdhcIq4K6DGTpYjtuyLD6giWbX'


def get_baiduApi_token():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'. \
        format(API_KEY, SECRET_KEY)
    response = requests.get(host)
    if response:
        access_token = response.json()['access_token']
        print(access_token)
        return access_token


'''
人像分割
'''


def request_image_classify(filepath, now_timestamp):
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_seg"
    # 二进制方式打开图片文件
    f = open(filepath, 'rb')
    img = base64.b64encode(f.read())

    output_dir = os.path.join(os.path.dirname(filepath), "image_classify_output_" + now_timestamp)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    params = {"image": img}
    # access_token = '24.0f9e6b1f730cdc4497f93f8605f3a92e.2592000.1670289258.282335-28272275'
    access_token = get_baiduApi_token()
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        output_base64 = response.json()["foreground"]
        img_data = base64.b64decode(output_base64)
        with open(os.path.join(output_dir, os.path.basename(filepath)), "wb") as fp:
            fp.write(img_data)
            print(os.path.join(output_dir, os.path.basename(filepath)), " success")


if __name__ == "__main__":
    now_timestamp = str(int(time.time()))
    dirname = r"C:\Users\10262\Desktop\contact\attend\pet_conf\0\tt0.top_0000.png"
    request_image_classify(dirname, now_timestamp)
#     for root, dirs, files in os.walk(dirname):
#         if os.path.abspath(root) == os.path.abspath(dirname):
#             for filename in files:
#                 request_image_classify(os.path.join(root, filename), now_timestamp)
