"""
Request对象   属性	说明
    method	请求方法，比如GET、POST
    data	以字符串的形式存储请求的数据
    *files	上传的文件，类型为MultiDict
    args	解析URL中提交的参数，类型为MultiDict
    form	上传的表单数据，类型为MultiDict
    values	包含args和form的数据，类型为CombineMultiDict
    *json	解析JSON数据，如果没有则返回None
    cookies	包含客户端传输的所有 cookies ，类型为MultiDict
    headers	请求头信息，类似字典，可通过关键词获取对应得信息

"""

from flask import Flask, request, render_template
import json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("request.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    print('request.method:\n', request.method)
    print('request.data:\n', request.data)
    print('request.request.args:\n', request.args)
    print("request.request.args.get('b'):\n", request.args.get('b'))
    print('request.form:\n', request.form)
    print("request.request.form.get('password'):\n", request.form.get('password'))
    print('request.values:\n', request.values)

    # Content-Type should be 'application/json'
    try:
        print('request.json:\n', request.json)
    except Exception as e:
        print(e)

    print('request.cookies:\n', request.cookies)
    print('request.headers:\n', request.headers)

    # 各种url
    print('url: ', request.url)
    print('base_url: ', request.base_url)
    print('host: ', request.host)
    print('host_url: ', request.host_url)
    print('path: ', request.path)
    print('full_path: ', request.full_path)

    return json.dumps(request.form)  # 将MultiDict数据处理为JSON数据


if __name__ == '__main__':
    app.run(debug=False)
