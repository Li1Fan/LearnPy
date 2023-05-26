import json

from flask import Flask, redirect, url_for, request, session, render_template

app = Flask(__name__)
app.secret_key = 'secret_key'

user_info = {'admin': '123',
             'guest': '123'
             }


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = json.loads(request.data.decode('utf-8'))
        print(f'data: {data}')
        if data['username'] not in user_info.keys():
            response = {'status': -1, 'msg': '用户不存在'}
            return json.dumps(response)
        elif data['password'] != user_info[data['username']]:
            response = {'status': -2, 'msg': '密码错误'}
            return json.dumps(response)
        # 设置会话中的用户信息
        session['username'] = data['username']
        session['password'] = data['password']
        response = {'status': 0, 'msg': '登录成功'}
        return json.dumps(response)
    return render_template('login.html')


@app.route('/logout')
def logout():
    # 删除会话中的用户信息
    session.pop('user')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
