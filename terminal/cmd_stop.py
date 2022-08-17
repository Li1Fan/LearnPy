# -*- coding: utf-8 -*-
import os
import signal
import subprocess
import time

import psutil

process = subprocess.Popen('busybox top', shell=True, cwd=os.getcwd())
pid = process.pid
# print(process.stdout)
time.sleep(5)
os.kill(pid, signal.SIGKILL)


# SIGILL
# SIGINT


def kill_iperf():
    for process in psutil.process_iter():
        try:
            cmdline = process.cmdline()
            if "iperf.exe" in str(cmdline):
                process.terminate()
            if "cmd.exe" in str(cmdline):
                process.terminate()
            if "adb.exe" in str(cmdline):
                process.terminate()
        except psutil.AccessDenied:
            pass
        except psutil.NoSuchProcess:
            pass
