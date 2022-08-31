import web

urls = (
    '/index/(.*)', 'index',
    '/upper/(.*)', 'upper',
    '/lower/(.*)', 'lower',
    '/(js|css|images)/(.*)', 'static'
)
app = web.application(urls, globals())
render = web.template.render('templates')


class index:
    def GET(self, text):
        return render.hello(content=text.upper())


class upper:
    def GET(self, text):
        web.header('Content-Type', 'text/html;charset=UTF-8')
        print('input:' + text)
        return text.upper()


class lower:
    def GET(self, text):
        web.header('Content-Type', 'text/html;charset=UTF-8')
        print('input:' + text)
        return text.lower()


class static:
    def GET(self, media, file):
        try:
            print('/static/' + media + '/' + file)
            f = open('static/' + media + '/' + file, 'rb')
            return f.read()
        except:
            return ''


if __name__ == "__main__":
    app.run()
