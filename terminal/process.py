# -*- coding: utf-8 -*-
import subprocess

"""
call
不需要交互
正常返回值为0，不引发异常
"""
# shell对于传参命令有影响，不需要传参命令不影响
cmd = 'ls -l'
ret = subprocess.call(cmd, shell=True)
print(ret)

cmd = ['ls', '-l']
ret = subprocess.call(cmd, shell=False)
print(ret)

cmd = 'echo 1'
ret = subprocess.call(cmd, shell=True)
print(ret)

cmd = ['echo', '1']
ret = subprocess.call(cmd, shell=False)
print(ret)

"""checkout会引发异常"""
cmd = 'echo value'
ret = subprocess.call(cmd, shell=True)
print(ret)

cmd = 'echo value'
ret = subprocess.check_output(cmd, shell=True)
print(ret)
print('-' * 10)

cmd = 'pri 1'
ret = subprocess.call(cmd, shell=True)
print(ret)

try:
    cmd = 'pri 1'
    ret = subprocess.check_output(cmd, shell=True)
    print(ret)
except Exception as e:
    print(e)

print('-' * 10)
"""
popen
"""
cmd = 'ls'
ret = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
print(ret.stdout.read().decode('utf-8'))
