import json
import hashlib


def tomac(mac):
    """输入字节类型的mac转为str类型带:格式,例: b'\x00\x0e\xc6\xb3\x83;' >> 00:0e:c6:b3:83:3b"""
    macstr = ''
    n = 0
    for i in tohex(mac):
        if n % 2 == 0 and n != 0:
            macstr += ':'
        macstr += i
        n += 1
    return macstr


def print_hex(bytes):
    """将字节一个个打印"""

    l = [hex(int(i)) for i in bytes]
    print(" ".join(l))
    return " ".join(l)


def tohex(a):
    """字符串转16进制字节 互转"""

    if type(a) is bytes:
        return bytes.hex(a)
    elif type(a) is str:
        return bytes.fromhex(a)


def toHex(num):
    """数字转16进制 例如:257 = 101 = 0x0101"""

    chaDic = {10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f'}
    hexStr = ""

    if num < 0:
        num = num + 2 ** 32

    while num >= 16:
        digit = num % 16
        hexStr = chaDic.get(digit, str(digit)) + hexStr
        num //= 16
    hexStr = chaDic.get(num, str(num)) + hexStr

    return hexStr


def intToBytes(value, length):
    """int转换byte 返回byte"""

    result = []
    for i in range(0, length):
        result.append(value >> (i * 8) & 0xff)
    result.reverse()
    result_bytes = bytes(result)
    return result_bytes


def SetMd5(_byte):
    """byte转换MD5 返回str"""

    md5hash = hashlib.md5(_byte)
    a = md5hash.hexdigest()
    i = 0
    s = str()
    while i < 8:
        s += a[i]
        i += 1
    return s


def CheckMd5(Md5, b):
    """校验MD5"""

    t_Md5 = SetMd5(b)  # 将byte转为str
    if Md5 == t_Md5:
        return True
    else:
        return False


def jtob(data):
    """组装payload使用"""

    # 将字典格式转为json格式,再转为byte
    json11 = json.dumps(data)
    json111 = json11.encode('GBK')
    return json111
