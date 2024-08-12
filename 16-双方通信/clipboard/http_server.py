from flask import Flask, request, render_template, render_template_string

app = Flask(__name__)

clipboard_text = ''
history_text = ''


# 初始页面
@app.route('/')
def index():
    return render_template('index.html', messages=clipboard_text, height=calculate_height(clipboard_text))


# 处理表单提交
@app.route('/', methods=['POST'])
def add_message():
    print(request.form)
    global clipboard_text
    global history_text
    if request.form['clear'] == '1':
        clipboard_text = ''
        history_text = ''
    else:
        message = request.form['message']
        clipboard_text = message
        history_text = history_text + str(get_current_time()) + ':\n' + message + '\n\n'
    # 重定向到首页
    return index()


@app.route('/text')
def text():
    return render_template_string('<head><meta charset="UTF-8"><title>剪贴板历史</title>'
                                  '<body><pre>{{ message }}</pre></body>', message=history_text)


def get_current_time():
    import time
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def calculate_height(content):
    height = content.count('\n') * 16 + 30
    if height < 160:
        height = 160
    return height


if __name__ == '__main__':
    print("192.168.222.108:80")
    app.run(host='0.0.0.0', port=8888, debug=True)
