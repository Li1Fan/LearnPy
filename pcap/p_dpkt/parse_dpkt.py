# -*- coding: utf-8 -*-
import binascii
import copy
import json
import struct

import dpkt
from scapy.layers.inet import IP

data = b"\x11\x22\x33\x00\x00\x00\x55\x66\x77\x00\x00\x00\x09\x13\x6d\x64\x35\x35\x10\x10\x00\x00\x22\x22\x00\x00\x00\x00\x00\x00\x00\x00\x00\x12\x7b\x22\x68\x65\x6c\x6c\x6f\x22\x3a\x20\x22\x77\x6f\x72\x6c\x64\x22\x7d"
# packet = struct.unpack_from("!6s6sH4sHI8sH", data)
"""dpkt解包"""
eth = dpkt.ethernet.Ethernet(data)
print(eth.data)
print(eth.dst)
print(eth.src)
print(eth.type)

"""struct解包"""
print(len(b'\x11'))
head = struct.Struct("!6s6sH4sHI8sH18s")
data_header = head.unpack_from(data)
print(data_header)
value = data_header[8].decode()
print(value, type(value))
print(json.loads(value), type(json.loads(value)))

print(len(data_header[0]))
c = binascii.hexlify(data_header[0])
print(c, type(c))
print(c, len(c))
d = binascii.unhexlify(c)
print(d, type(d))

e = bytes('112233000000', encoding='utf-8')
print(e, len(e))
print(hex(16))

"""scapy"""
# pcap = copy.deepcopy(data)
# # print(pcap)
# print(pcap[IP].src, type(pcap[IP].src))
# pcap[IP].src = '192.0.2.1'
# pcap[IP].dst = '11.22.33.44'
mac = 'e454e8c88de9'
print(binascii.unhexlify(mac))
