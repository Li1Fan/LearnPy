from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

message = ''


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.form)
        global message
        if request.form['clear'] == '1':
            message = ''
        else:
            message = message + str(get_current_time()) + ':\n' + request.form['message'] + '\n\n'
        return redirect(url_for('index'))

    # 设置了一个隐藏的清空剪贴板的按钮，当点击这个按钮时，会将clear的值设置为1，然后提交表单，这样就可以清空剪贴板了
    return '''
            <h1>在线剪贴板</h1>
            <form method="POST">
                <label for="message">输入信息：</label>
                <br><br>
                <textarea id="message" name="message" rows="15" cols="60" autocomplete="off" style='border-color:black;border-width:3px;'>
                </textarea><br>
                <br>
                <input type="submit" value="发送">
                <br><br>
                <input type="button" value="清空剪贴板" onclick="document.getElementById('clear').value='1';
                this.form.submit();">
                <input type="button" value="剪贴板历史" onclick="window.open('/text', '_blank');">
                <input type="hidden" id="clear" name="clear" value="0">
            </form>
            '''


@app.route('/text')
def text():
    return render_template_string('<pre>{{ message }}</pre>', message=message)


def get_current_time():
    import time
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234, debug=True)
