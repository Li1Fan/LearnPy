import psutil

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
    except:
        pass
