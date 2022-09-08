# -*- coding: utf-8 -*-
import re

data = '张三:110李四:119王五:120'
pattern = re.compile(r'([^:^\d]*):', re.I)
print(pattern.findall(data))

print()