import requests

res=requests.get('http://127.0.0.1:8000')
res.encoding='utf-8'
print(res.status_code)
print(res.content)
print(res.cookies.get_dict())