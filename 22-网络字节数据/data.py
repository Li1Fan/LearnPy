import binascii
import struct

data_int = 42
data_float = 3.14
date_str = "hello"

# 整数（4 字节），再打包一个浮点数（4 字节），最后打包一个字符串（5 字节），总共 13 字节
byte_stream = struct.pack('if5s', data_int, data_float, date_str.encode('utf-8'))
print("打包后的字节流:", byte_stream)

# 将字节流转换为十六进制格式
hex_format = byte_stream.hex()
print("字节流的十六进制格式:", hex_format)

# 将字节数据转换为十六进制字符串
hex_string = binascii.hexlify(byte_stream).decode('utf-8')

print("字节数据的十六进制字符串:", hex_string)

for i in range(0, len(hex_string), 2):
    print(hex_string[i:i + 2], end=' ')

# 计算字节流所占的字节数
byte_count = len(byte_stream)
print("打包后字节流所占的字节数:", byte_count)

# 解包数据
unpacked_data = struct.unpack('if5s', byte_stream)

print("解包后的数据:", unpacked_data)