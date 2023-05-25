from flask import Flask, request, redirect
from flask import url_for

app = Flask(__name__)


@app.route('/')
def index():
    return 'index'


@app.route('/login')
def login():
    print(f"in login function, request.values: {request.values}")
    return 'login'


@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'


"""
url_for()函数用于构建指定函数的URL。
它把函数名称作为第一个参数。
它可以接受任意个关键字参数，每个关键字参数对应 URL 中的变量，未知变量 将添加到 URL 中作为查询参数。
"""

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)  # 运行app
