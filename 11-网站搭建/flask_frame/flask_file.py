"""
如果想要更改路径，可以在初始化Flask实例时进行修改
app = Flask(__name__, static_folder='', template_folder='')
默认app.py与templates和static文件夹同级目录。
"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    int_ = 1024
    str_ = 'Hello World!'
    list_ = [1, 2, 3, 4, 5]
    dict_ = {'name': 'flask', 'age': 23}
    # render_template方法:渲染模板
    # 参数1: 模板名称  参数n: 传到模板里的数据
    return render_template('file.html', my_int=int_, my_str=str_, my_list=list_, my_dict=dict_)


if __name__ == '__main__':
    app.run(debug=True)
