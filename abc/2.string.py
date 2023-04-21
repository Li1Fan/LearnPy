import re
from difflib import SequenceMatcher

text = '您好，您拨打的电话正在通话中。'
print(text)
# 文本替换
a = re.compile(r'[,.，。]').sub('', text)
print(a)

print(text.replace('，', '').replace('。', ''))

# 文本切割
b = re.compile(r'(\s?)').split(a)
print(b)
c = re.compile(r'(.*?)').findall(a)
print(f'c: {c}')

# 文本组合，c为列表
print(''.join(c))


def split2list(text: str) -> list:
    """

    :param text:
    :return:
    """
    lst = re.compile(r'(\s?)').split(a)
    return list(filter(None, lst))


print(split2list(text))

# split切割会产生空字符问题
x = "[1 2 3 4][2 3 4 5]"
y = "1 2 3 4][2 3 4 5"
p = re.compile(r'[^\d]+')
print(p.split(x))
print(p.split(y))

# 解决上述问题
print([i for i in p.split(x) if i])  # 列表生成式
print(list(filter(lambda a: a, p.split(x))))  # filter
print(list(filter(None, p.split(x))))
print(re.compile(r'\d').findall(x))  # 一开始就使用findall


# 字符串匹配百分比
def percentage_match(expect_str, real_str, percent=0.8):
    """
    2个字符串模糊匹配，得到匹配百分比
    :param expect_str: 预期字符串
    :param real_str: 实际字符串
    :param percent: 预期应该至少达到的百分比
    :return:
    """
    m = SequenceMatcher(None, expect_str, real_str)
    real_percent = m.ratio()
    print(real_percent)
    if real_percent >= percent:
        return True
    return False


percentage_match('自定义彩铃音', '')
