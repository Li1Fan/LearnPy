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
    print(1)
    # print('request.json:\n', request.json)
    print(2)
    print('request.cookies:\n', request.cookies)
    print('request.headers:\n', request.headers)
    return json.dumps(request.form)  # 将MultiDict数据处理为JSON数据


if __name__ == '__main__':
    app.run(debug=False)
