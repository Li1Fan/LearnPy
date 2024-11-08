XPath 是一种用于在 XML 和 HTML 文档中查找和选择节点的语言。它提供了一种灵活的方法来访问和操作文档结构。以下是 XPath 的基本使用语法和常见表达式。

### 基本语法

1. **路径表达式**
   - 使用 `/` 符号表示路径，根节点用单斜杠 `/` 表示。
   - 示例: `/html/body/p` 选择文档中的所有 `<p>` 元素。

2. **相对路径**
   - 使用 `//` 可以选择文档中匹配指定节点的所有元素，不管其位置。
   - 示例: `//div` 选择文档中的所有 `<div>` 元素。

3. **节点选择**
   - 可以通过节点名、属性、索引等方式选择节点。

### 常见 XPath 表达式

1. **选择所有节点**
   - 表达式: `//*`
   - 示例: 选择文档中的所有节点。

2. **选择特定标签**
   - 表达式: `//tagname`
   - 示例: `//a` 选择所有 `<a>` 标签。

3. **选择具有特定属性的节点**
   - 表达式: `//tagname[@attribute='value']`
   - 示例: `//input[@type='text']` 选择所有类型为 `text` 的 `<input>` 元素。

4. **选择子节点**
   - 表达式: `//parenttag/childtag`
   - 示例: `//ul/li` 选择所有 `<ul>` 下的 `<li>` 标签。

5. **选择父节点**
   - 表达式: `//childtag/..`
   - 示例: `//li/..` 选择所有 `<li>` 的父节点。

6. **使用位置**
   - 表达式: `//tagname[position()=n]`
   - 示例: `//li[position()=1]` 选择第一个 `<li>` 元素。

7. **选择最后一个节点**
   - 表达式: `//tagname[last()]`
   - 示例: `//li[last()]` 选择最后一个 `<li>` 元素。

8. **条件选择**
   - 表达式: `//tagname[@attribute]`
   - 示例: `//input[@disabled]` 选择所有 `disabled` 属性的 `<input>` 元素。

9. **包含子字符串的选择**
   - 表达式: `//tagname[contains(@attribute, 'substring')]`
   - 示例: `//a[contains(@href, 'example')]` 选择所有 `href` 属性中包含 `example` 的 `<a>` 标签。

### 示例代码

以下是一个 Python 示例，展示如何使用 XPath：

```python
from lxml import html
import requests

# 获取网页内容
url = 'http://example.com'  # 替换为你想抓取的网页
response = requests.get(url)
tree = html.fromstring(response.content)

# 示例: 获取所有 <a> 标签
links = tree.xpath('//a')
print("所有链接:", links)

# 示例: 获取 ID 为 'header' 的元素
header = tree.xpath('//*[@id="header"]')
print("ID 为 'header' 的元素:", header)

# 示例: 获取所有具有 'class' 属性的 <div> 标签
divs_with_class = tree.xpath('//div[@class]')
print("所有具有 'class' 属性的 <div> 标签:", divs_with_class)

# 示例: 获取第一个 <li> 标签的文本
first_li_text = tree.xpath('//li/text()')[0] if tree.xpath('//li/text()') else "没有找到 <li> 标签"
print("第一个 <li> 标签的文本:", first_li_text)
```

### 结论

XPath 是一个功能强大的工具，可以帮助你高效地解析和提取 XML 和 HTML 文档中的信息。掌握其基本语法和常见用法，将大大提高数据处理的效率。如果你有其他具体问题或需要更深入的讲解，欢迎随时询问！