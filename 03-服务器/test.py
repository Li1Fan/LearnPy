# -*- coding: utf-8 -*-
import binascii

from scapy.volatile import RandMAC

mac = RandMAC()
mac_b = binascii.unhexlify(str(mac).replace(":", ""))
print(mac_b, len(mac_b), type(mac_b))
