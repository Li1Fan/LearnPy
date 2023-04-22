# -*- coding: utf-8 -*-
import threading

from pcap.p_capture.send_pacp.rawSocket import RawSocket

global a
a = 1


def input_s():
    global a
    a = int(input())


t = threading.Thread(target=input_s, )
t.start()

raw = RawSocket('enp1s0')
# raw.run()
t_recv = threading.Thread(target=raw.start, )
t_recv.start()

while a != 0:
    packet = raw.recv()

    try:
        print(packet)
    except:
        pmessage = None
        continue
raw.stop()
