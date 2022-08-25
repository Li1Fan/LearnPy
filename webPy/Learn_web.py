import web

urls = (
    '/', 'index',
    '/conf/(.*)', 'conf',
    '/head/.*', 'head',
    '/favicon.ico', 'icon'
)

app = web.application(urls, globals())
"""两种传参方式
？name=jack&id=1
/(.*)圆括号表示捕捉对应的数据"""


class index:
    def GET(self):
        render = web.template.render('templates/')
        # i = web.input(name=None)
        # return render.index(i.name)
        return render.index()


class conf:
    def GET(self, name):
        render = web.template.render('templates/')
        return render.index(name)


class head:
    def GET(self):
        return web.ctx.env


class icon:
    def GET(self):
        return web.seeother('/static/res/icon.ico')


if __name__ == "__main__":
    app.run()
