from scapy.config import conf
from scapy.layers.l2 import getmacbyip, arping, Ether, ARP

# print(getmacbyip('192.168.222.141'))

# IP_TEST = '10.27.106.'
# list_ip_none = []
# for i in range(255):
#     ip = IP_TEST + str(i)
#     mac_add = getmacbyip(ip)
#     if not mac_add:
#         print(ip)
#         list_ip_none.append(ip)
# print(list_ip_none)
if __name__ == '__main__':
    result = arping('192.168.31.1', timeout=1, verbose=False, multi=True)
    print(result[0].res, type(result[0].res), len(result[0].res))
    data = list()
    padding = 0

    for s, r in result[0].res:
        manuf = conf.manufdb._get_short_manuf(r.src)
        manuf = "unknown" if manuf == r.src else manuf
        padding = max(padding, len(manuf))
        data.append((r[Ether].src, manuf, r[ARP].psrc))

    for src, manuf, psrc in data:
        print("%-17s %-*s %s" % (src, padding, manuf, psrc))
    # IP_TEST = '192.168.222'
    # list_ip_none = []
    # for i in range(255):
    #     ip = IP_TEST + str(i)
    #     result = arping(ip, timeout=1, verbose=True, multi=True)
    #     print(result)
    # result = getmacbyip('192.168.222.91')
    # print(result)
