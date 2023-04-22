import re
import threading
import time

from scapy.layers.l2 import arping, Ether

ip_mac_map = dict()
known_device_list = ['88:c3:97:0c:5e:0e', '6e:e8:f3:da:56:b8', '42:03:61:f9:e9:e1']

# '70-c9-4e-de-5c-af' 这个有可能是路由器的
# 'c2:91:88:98:45:6e'


def arp_get_mac_by_ip(ip):
    result = arping(ip, timeout=10, verbose=False, multi=True)
    # print(result[0].res)
    if len(result[0].res) == 0:
        return None
    for query, answer in result[0].res:
        return (answer[Ether].src)


def arp_get_mac_by_gateway(gateway):
    gate = re.split(r'(.*)\d', gateway)[1]
    for i in range(1, 255):
        ip = gate + str(i)
        thread_arp = threading.Thread(target=get_mac, kwargs={'ip': ip})
        thread_arp.start()

    time.sleep(12)
    return ip_mac_map


def get_mac(ip):
    mac = arp_get_mac_by_ip(ip)
    if mac:
        ip_mac_map.update({ip: mac})


if __name__ == "__main__":
    a = arp_get_mac_by_gateway('192.168.31.1')
    print(a)
    for ip, mac in a.items():
        if mac not in known_device_list:
            print('未知设备：{} {}'.format(ip, mac))
