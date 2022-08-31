# _*_coding:utf-8_*_
# !/usr/bin/env python

from wsgiref.simple_server import make_server


# 定义application函数:
def application(environ, start_response):
    print(environ)
    start_response('200 OK', [('Content-Type', 'text/html')])

    f = open('test.html', 'rb')
    return [f.read()]


# 创建一个服务器，IP地址为空，端口是8000，处理函数是application:
httpd = make_server('', 8000, application)
print('Serving HTTP on port 8000...')
# 开始监听HTTP请求:
httpd.serve_forever()
