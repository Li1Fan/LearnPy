import requests
import re
"""模拟浏览器的登录github
"""
# 访问登录页面
r1 = requests.get('https://github.com/login/',
                  headers={
                      'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'},

                  )

authenticity_token = re.findall(r'name="authenticity_token".*?value="(.*?)"', r1.text, re.S)[0]
print(authenticity_token)
print(r1.cookies.items())  # 获取列表类型的cookies信息
print(r1.cookies.get_dict())  # 获取字典类型的cokies信息
cookies = r1.cookies.get_dict()
#
# # 访问登录页面
# r2 = requests.post('https://github.com/session',
#                    data={
#                        'commit': 'Sign in',
#                        'utf8': '?',
#                        'authenticity_token': authenticity_token,
#                        'login': '13220198866@163.com',
#                        'password': '123.com'},
#                    headers={
#                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'},
#                    cookies=cookies)
#
# # 访问设置个人主页
# cookies2 = r2.cookies.get_dict()  # 获取登录页面返回的cokies信息
# r3 = requests.get('https://github.com/settings/emails', cookies=cookies2)
#
# print('13220198866@163.com' in r3.text)

"""每次写爬虫都要在响应头中获取cokies信息，然后在把获取的cokies信息加在请求头，太繁琐了；
如果有了 requests.session()对象，就可以自动处理cokies问题了
"""
# session = requests.session()  # 相当于设置了 一个会话相关的容器，把所有会话相关的cookie都存放起来（自动保存cookie问题）
# r1 = session.get('https://github.com/login/',
#                  headers={
#                      'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'},
#
#                  )
#
# authenticity_token = re.findall(r'name="authenticity_token".*?value="(.*?)"', r1.text, re.S)[0]
