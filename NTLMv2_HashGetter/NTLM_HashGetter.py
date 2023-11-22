import struct  # 用来处理字节数据
import base64
import binascii
import string
import argparse


# 解析获取到的 buffer_info，返回大小及偏移信息
def getBufferInfo(info_data):
    length = struct.unpack("h", info_data[0:2])[0]  # short型
    offset = struct.unpack("l", info_data[4:8])[0]  # long 型

    return (length, offset)


# 将字节串转为 string 型的 字符串
def toHex(byte_data):
    return binascii.hexlify(byte_data).decode("utf-8")


# 根据给定的 len , offset 提取数据
def getData(data, length, offset):
    return data[offset : offset + length]


# 除去不可见字符
def remove_invisible_chars(text):
    visible_chars = set(string.printable)
    filtered_text = "".join(char for char in text if char in visible_chars)
    return filtered_text


# 根据给出的协议内容自动得到 hash
def getHash(data1, data2):
    # 自动判断两个数据的类型
    for message in data1, data2:
        # 解码base64
        message = base64.b64decode(message)

        # 从质询中提取 challenge
        if message[8] == 2:
            challenge_code = toHex(message[24:32])
            # print(challenge_code)

        # 消息答复质询，包含响应
        if message[8] == 3:
            # 获取安全缓冲区长度及偏移地址
            response_info = message[20:28]
            domain_name_info = message[28:36]
            user_name_info = message[36:44]
            # 从上面获取的数据中提取长度和偏移地址信息
            response_len, response_offset = getBufferInfo(response_info)
            domain_name_len, domain_name_offset = getBufferInfo(domain_name_info)
            user_name_len, user_name_offset = getBufferInfo(user_name_info)

            # 转化为可读的形式
            user_name = remove_invisible_chars(
                getData(message, user_name_len, user_name_offset).decode("utf-8")
            )
            domain_name = remove_invisible_chars(
                getData(message, domain_name_len, domain_name_offset).decode("utf-8")
            )

            response = toHex(getData(message, response_len, response_offset))
            proofstr = response[0:32]
            response = response[32:]

            # print(user_name, domain_name)
            # print(proofstr)
            # print(response)

    # 输出
    print(f"{user_name}::{domain_name}:{challenge_code}:{proofstr}:{response}")


# ntml_data = input("[*] input your NTMLv2 data:\n")
ntml_data = "TlRMTVNTUAADAAAAGAAYAIIAAABYAVgBmgAAABIAEgBYAAAACAAIAGoAAAAQABAAcgAAABAAEADyAQAAFYKI4goAYUoAAAAPVS6RhfnytMqt5hsgL2wgnFcASQBEAEcARQBUAEwATABDAGoAYQBjAGsAQwBMAEkARQBOAFQAMAAxAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAC0dJFcrFf5UQENDHFmWXTABAQAAAAAAAAQNlisC7dkB5plBR9ajSvIAAAAAAgASAFcASQBEAEcARQBUAEwATABDAAEACABEAEMAMAAxAAQAJABXAGkAZABnAGUAdABMAEwAQwAuAEkAbgB0AGUAcgBuAGEAbAADAC4ARABDADAAMQAuAFcAaQBkAGcAZQB0AEwATABDAC4ASQBuAHQAZQByAG4AYQBsAAUAJABXAGkAZABnAGUAdABMAEwAQwAuAEkAbgB0AGUAcgBuAGEAbAAHAAgABA2WKwLt2QEGAAQAAgAAAAgAMAAwAAAAAAAAAAAAAAAAMAAAB4zcUgkQdiJn5ASItgAyg1xqN2BNHpvj7O5YgC+1+RUKABAAAAAAAAAAAAAAAAAAAAAAAAkAIABIAFQAVABQAC8AMQA5ADIALgAxADYAOAAuADAALgAxAAAAAAAAAAAAlbkMmv5SCuQVUPyZtIn4uA=="
challenge_data = "TlRMTVNTUAACAAAAEgASADgAAAAVgoniKvcbXKckYmgAAAAAAAAAALQAtABKAAAACgA5OAAAAA9XAEkARABHAEUAVABMAEwAQwACABIAVwBJAEQARwBFAFQATABMAEMAAQAIAEQAQwAwADEABAAkAFcAaQBkAGcAZQB0AEwATABDAC4ASQBuAHQAZQByAG4AYQBsAAMALgBEAEMAMAAxAC4AVwBpAGQAZwBlAHQATABMAEMALgBJAG4AdABlAHIAbgBhAGwABQAkAFcAaQBkAGcAZQB0AEwATABDAC4ASQBuAHQAZQByAG4AYQBsAAcACAAEDZYrAu3ZAQAAAAA="

if __name__ == "__main__":
    # getHash(ntml_data, challenge_data)
    parser = argparse.ArgumentParser(
                    prog='NTLM_HashGetter',
                    description='Get NTLMv2 hash from NTLM protocol content',
                    epilog='Text at the bottom of help')
    # parser.print_help()
    
    parser.add_argument('-d', '--data', nargs='*', help='NTLMv2 protocol content')
    
    # 检查参数
    args = parser.parse_args()
    
    if (len(args.data) == 2):
        getHash(args.data[0], args.data[1])
    else:
        print("[-] 参数错误")
        parser.print_help()