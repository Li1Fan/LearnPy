import json

from flask import Flask, redirect, url_for, request, session, render_template

app = Flask(__name__)
# 设置密钥
app.secret_key = 'secret_key'
# 设置session的过期时间
app.permanent_session_lifetime = 60 * 10

# 设置用户信息
user_info = {'admin': '123',
             'guest': '123'}


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(f'form: {request.form}')
        print(f'cookies: {request.cookies}')  # cookies存储在客户端，session存储在服务端，session的ID存储在客户端的cookies中
        # 判断用户的登录状态
        username = session.get('username')
        if username:
            return redirect(url_for('main'))
        return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/login/verify', methods=['GET', 'POST'])
def login_verify():
    if request.method == 'POST':
        # 请求数据
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


@app.route('/logout')
def logout():
    # 删除会话中的用户信息
    session.pop('username')
    return redirect(url_for('index'))


@app.route('/main')
def main():
    # 判断用户的登录状态
    username = session.get('username')
    if username:
        return '登录用户是:' + username + '<br>' + "<b><a href = '/logout'>点击这里注销</a></b>"
    return redirect(url_for('login'))


if __name__ == '__main__':
    # debug设置为True，修改代码后，服务器会自动重启
    app.run(debug=True)
