# -*- coding: utf-8 -*-
import os
import signal
import subprocess
import time

process = subprocess.Popen('busybox top', shell=True, cwd=os.getcwd())
pid = process.pid
# print(process.stdout)
time.sleep(5)
os.kill(pid, signal.SIGKILL)
