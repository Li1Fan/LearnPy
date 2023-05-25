from flask import Flask
from markupsafe import escape

app = Flask(__name__)  # 在当前文件下创建应用


@app.route("/")  # 装饰器，url，路由
def index():  # 视图函数
    return "hello world"


@app.route("/say_hello/<name>")  # 装饰器，url，路由
def say_hello(name):  # 视图函数
    return "hello world,I am your friend %s" % name


"""
string  （缺省值） 接受任何不包含斜杠的文本
int     接受正整数
float   接受正浮点数
path    类似 string ，但可以包含斜杠
uuid    接受 UUID 字符串
"""


@app.route('/user/<username>')
def show_user_profile(username):
    return f'User {escape(username)}'
    # escape()函数可以对输入的内容进行转义，防止恶意攻击，比如输入<script>alert('hello')</script>，会弹出一个对话框


@app.route('/post/<int:post_id>')  # int类型的参数，只接受整数，如果不是整数，会返回404
def show_post(post_id):
    return f'Post {post_id}'


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    return f'Subpath {escape(subpath)}'


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)  # 运行app
