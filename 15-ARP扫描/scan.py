from scapy.layers.l2 import ARP, Ether, srp

my_mac = {"苹果14": "a6:6c:05:18:3a:1a",
          "电脑": "7c:76:35:66:ff:03",
          "网关": "88:c3:97:0c:5e:0e",
          "天猫精灵": "10:9e:3a:6b:dc:63",
          "路由器": "66:e4:98:ab:e8:c9"}
dang_mac = {"1": "70:c9:4e:de:5c:af",
            "2": "c2:91:88:98:45:6e"}
all_mac = []

# 构造 ARP 请求数据包
arp = ARP(pdst='192.168.31.0/24')

# 构造以太网帧
ether = Ether(dst='ff:ff:ff:ff:ff:ff')

# 发送数据包并等待响应
ans, _ = srp(ether / arp, timeout=2, verbose=False)

# 遍历所有已响应设备，输出 IP 和 MAC 地址信息
for _, pkt in ans:
    mac_addr = pkt[ARP].hwsrc
    ip_addr = pkt[ARP].psrc
    # print(f'IP 地址：{ip_addr}，MAC 地址：{mac_addr}')
    all_mac.append({ip_addr: mac_addr})
    if mac_addr not in my_mac.values():
        print('未知设备：{} {}'.format(ip_addr, mac_addr))

print(dang_mac)
for i in all_mac:
    print(i)
