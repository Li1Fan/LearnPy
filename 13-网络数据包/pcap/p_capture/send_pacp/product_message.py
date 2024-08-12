import struct
import binascii
import json

# from src.log.Log import log
# from src.util.socketutil import intToBytes, tohex, SetMd5
from pcap.p_capture.send_pacp.socketutil import intToBytes, SetMd5, tohex


def set_md5(action, session, sad, length, payload):
    """
    body加密
    :param action:
    :param session:
    :param sad:
    :param length:
    :param payload:
    :return:
    """
    info_body = intToBytes(action, 2) + intToBytes(session, 4) + sad + intToBytes(length, 2) + payload
    md5 = tohex(SetMd5(info_body))
    return md5


"""
数据报文填充 0x00， 满足以太网最小包 64 字节
payload : 字节数据缓冲
"""


def fill_payload(payload):
    length = len(payload)
    if length < 26:
        b0 = 26 - length
        for i in range(b0):
            payload += b'\x00'
    return payload


def composevlanpacket(dmac, smac, vtype, vlanid, protocol, action, session, sad, payload):
    """
    组成二层vlan报文
    :param dmac:
    :param smac:
    :param vtype:
    :param vlanid:
    :param protocol:
    :param action:
    :param session:
    :param sad:
    :param payload:bytes
    :return:
    """
    dmac_b = binascii.unhexlify(dmac.replace(':', ''))
    smac_b = binascii.unhexlify(smac.replace(':', ''))
    payload_b = payload
    length = len(payload_b)
    payload_b = fill_payload(payload_b)
    payload_l = len(payload_b)
    # MD5加密
    md5 = set_md5(action, session, sad, length, payload_b)
    # packet = None
    # 构造二进制数据
    if vlanid != 0:
        packet = struct.pack("!6s6sHHH4sHI8sH" + str(payload_l) + "s", dmac_b, smac_b, vtype, vlanid, protocol,
                             md5, action, session, sad, length, payload_b)
    else:
        packet = struct.pack("!6s6sH4sHI8sH" + str(payload_l) + "s", dmac_b, smac_b, protocol,
                             md5, action, session, sad, length, payload_b)
    return packet


"""
Message format:
0 : dmac      : ff:ff:ff:ff:ff:ff
1 : smac
2 : vlan type : 0x8100
3 : vlan id
4 : protocol  : 0x9700
5 : md5       : 4 bytes
6 : action    : 2 bytes
7 : session   : 
8 : sad       :
9 : length    :
10: payload   : json format
"""


class PMessage(object):
    """
    对外使用变量：
        smac : 发送MAC地址，例如 e4:54:e8:9a:4b:51
        dmac : 目的MAC地址
        vlan_id : 消息使用的 vlan_id，用来索引设备对象
        payload : json 格式的字符串
        session : 该消息对应的序列号
        action  : 该消息对应的类型
        device  : 引用 Device 对象，确认改消息是哪个设备发送的
    """

    def __init__(self, session):
        self.smac = '8c:ec:4b:6c:8a:79'
        self.dmac = 'ff:ff:ff:ff:ff:ff'
        self.protocol = 0x9700
        self.action = 0x0101
        self.session = session
        self.sad = b'\x00\x00\x00\x00\x00\x00\x00\x00'
        self.payload = ''
        self.device = None
        self.vlan_id = 1
        self.callback = None

    def equal(self, other):
        if self.smac != other.smac:
            return False
        if self.dmac != other.dmac:
            return False
        if self.action != other.action:
            return False
        if self.session != other.session:
            return False
        if self.payload != other.payload:
            return False
        return True

    def tostr(self):
        return "'smac': {},'dmac': {},'action': {},'session': {},'vlan': {}\t 'payload': {}".format(
            self.smac, self.dmac, hex(self.action), self.session, self.vlan_id, self.payload
        )

    def raw(self):
        return composevlanpacket(self.dmac, self.smac, 0x8100, self.vlan_id,
                                 self.protocol, self.action, self.session, self.sad, self.payload)

    @staticmethod
    def from_bytes(bytes_info):
        MIN_BYTES = 34
        if bytes_info is None:
            return None
        if len(bytes_info) < MIN_BYTES:
            return None
        offset = MIN_BYTES
        vlan_ofs = 0
        msg_ofs = 0
        pos12 = int(bytes_info[12])
        pos13 = int(bytes_info[13])
        has_vlan = (pos12 == 0x81 and pos13 == 0x00)
        if has_vlan:
            vlan_ofs = 4
            offset += 4
            msg_ofs = 2
        pro1 = int(bytes_info[12 + vlan_ofs])
        pro2 = int(bytes_info[13 + vlan_ofs])
        has_pro = (pro1 == 0x97 and pro2 == 0x00)
        if has_pro is False:
            return None
        # log.info('recv raw packet : {}'.format(bytes_info))
        msg = PMessage(0)
        raw_msg = None
        length = len(bytes_info) - offset
        if has_vlan:
            raw_msg = struct.unpack('!6s6sHHH4sHI8sH' + str(length) + "s", bytes_info)
        else:
            raw_msg = struct.unpack('!6s6sH4sHI8sH' + str(length) + "s", bytes_info)
        # log.info('recv raw msg {}'.format(raw_msg))
        msg.dmac = "%02x:%02x:%02x:%02x:%02x:%02x" % struct.unpack("BBBBBB", raw_msg[0])
        msg.smac = "%02x:%02x:%02x:%02x:%02x:%02x" % struct.unpack("BBBBBB", raw_msg[1])
        msg.protocol = raw_msg[2 + msg_ofs]
        msg.action = raw_msg[4 + msg_ofs]
        msg.session = raw_msg[5 + msg_ofs]
        msg.length = raw_msg[7 + msg_ofs]
        if msg.length < 64:
            msg.payload = raw_msg[8 + msg_ofs].rstrip(b'\x00')
        else:
            msg.payload = raw_msg[8 + msg_ofs].rstrip(b'\x00')
        msg.payload = msg.payload.replace(b'""""', b'""')
        try:
            payload = json.loads(msg.payload.decode())
        except:
            # log.error(traceback.format_exc())
            # log.info('错误报文:{}'.format(msg.tostr()))
            return msg
        if 'vlan_id' in payload:
            msg.vlan_id = payload['vlan_id']
        else:
            msg.vlan_id = 0
        return msg


if __name__ == "__main__":
    msg0 = PMessage(0x1010)
    msg0.action = 0x100
    msg0.payload = json.dumps({'name': 'jack'})
    raw_bytes = msg0.raw()
    print(raw_bytes)
    print('find -----')
    if b'\x97\x00' in raw_bytes:
        print("find 0x9700")
    msg1 = PMessage.from_bytes(raw_bytes)
    print(msg1.tostr())
    if msg0.equal(msg1):
        print("PMessage unpack and pack success")
    else:
        print("PMessage unpack and pack failed")

    a = ''
    raw_bytes = b'\x8c\xecKl\x8ay \x93M\x85\xfb\xe3\x97\x00\x8f@\xc6\xbc\x01\x02\x00\x00\x00\x01NULL\x00\x00\x00\x00\x00/{"name":"D31","version":"2.0.8.22","vlan_id":5}'
    msg1 = PMessage.from_bytes(raw_bytes)
    print(msg1.tostr())
