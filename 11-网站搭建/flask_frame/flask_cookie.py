"""
Cookie以文本文件的形式存储在客户端的计算机上。
其目的是记住和跟踪与客户使用相关的数据，以获得更好的访问者体验和网站统计信息。
比如网站为了辨别用户身份、进行会话跟踪需要把一些数据 (例如：登录状态、用户名称) 储存在用户本地终端上，这些数据被称为 Cookie。
"""

from flask import Flask, request, Response, render_template, make_response, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return redirect(url_for('set_cookie'))  # 重定向响应的URL


# 获取cookie
@app.route('/get_cookie')
def get_cookie():
    cookie = request.cookies.get('user')  # 获取关键字为user对应cookie的值
    print(cookie)
    return render_template('get_cookie.html', cookie=cookie)


# 设置cookie
@app.route('/set_cookie')
def set_cookie():
    html = render_template('set_cookie.html')
    response = make_response(html)  # 设置响应体
    # response = Response(html)
    response.set_cookie('user', 'flask')
    return response


# 删除cookie
@app.route('/del_cookie')
def del_cookie():
    html = render_template('set_cookie.html')
    response = Response(html)
    response.delete_cookie('user')
    return response


if __name__ == '__main__':
    app.run(debug=True)
