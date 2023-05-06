import lxml.html
from lxml import etree

html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Study</title>
</head>
<body>
    <h1>java</h1>
    <p href="https://blog.csdn.net/qq_41220451" class="p1">python</p>
    <p href="https://blog.csdn.net/qq_41220451">c</p>
    <a>c++</a>
    <a>html</a>
    <a>html2</a>
    <a>css</a>
</body>
</html>
"""
html = etree.HTML(html)
# 所有p标签
p = html.xpath('//p')
print(p)
# print(p[0].tag)
# print(lxml.html.tostring(p[0]))

# 顺着节点找到p标签
p = html.xpath('/html/body/p')
print(p)

# 当前节点后代里面找 a 标签
a = html.xpath('/descendant::a')
print(a)

# 获取p标签中的href属性值
p = html.xpath('/html/body/p/@href')
print(p)

# 获取所有a标签的文本内容
a = html.xpath('/html/body/a/text()')
print(a)

# 获取p标签中class属性为p1的标签的文本内容
p = html.xpath('/html/body/p[@class="p1"]/text()')
print(p)

# 获取内容为python的p标签
p = html.xpath('/html/body/p[text()="python"]')
print(p)

a = html.xpath('/html/body/a[2]')
print(lxml.html.tostring(a[0]))

"""
#查看标签属性
html.xpath('/html/body/p/@href')
#查看标签文本
html.xpath('/html/body/a/text()')
#属性筛选
html.xpath('/html/body/p[@class="p1"]/text()')
#文本筛选
html.xpath('/html/body/p[text()="python"]')
#位置筛选
html.xpath('/html/body/a[2]')
"""
