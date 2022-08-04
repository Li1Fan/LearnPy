# -*- coding: utf-8 -*-
# 毫秒延时
import time

delay_mark = time.time()
while True:
    offset = time.time() - delay_mark
    print(offset)
    if offset > 0.0011:
        break
