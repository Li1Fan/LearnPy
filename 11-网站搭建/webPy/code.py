# -*- coding: utf-8 -*-
import web

# 网站目录结构
urls = (
    '/', 'index',
    '/favicon.ico', 'ico',
    # '/hello/(.*)', 'sayHello',
    '/hello', 'sayHello',
    '/add', 'add',
    '/99', 'multiply',
    '/form', 'form'
)
# 使用render到模板目录中去查找相应模板
render = web.template.render('templates/')
# 也可以使用frender直接找到指定模板
hello = web.template.frender('templates/hello.html')
multi = web.template.frender('templates/multi.html')
index_page = web.template.frender('templates/index.html')
form_page = web.template.frender('templates/form.html')


class index:
    def GET(self):
        return index_page()


class ico:
    def GET(self):
        return web.seeother('/static/res/pygame.ico')


class sayHello:
    # def GET(self, name):
    #     i = web.input(name=None)  # 可以直接传入，也可以使用属性?name=Bob传入
    #     name = i.name
    #     # 以下两种均可
    #     # return render.hello(name)
    #     return hello(name)
    def GET(self):
        return hello('')


class add:
    def POST(self):
        i = web.input()
        print(i.title)
        # n = db.insert('todo', title=i.title)
        raise web.seeother('/hello')


class multiply:
    def GET(self):
        return multi()


class form:
    def GET(self):
        value = web.input()
        print("value:{}".format(value))
        return form_page()

    def POST(self):
        data = web.input()
        print(data)
        raise web.seeother('/form?data={}'.format(data.fruit.encode('utf-8').decode('latin1')))


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
