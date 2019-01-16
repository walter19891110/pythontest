# -*- coding:utf-8 -*-

#客户端
import socket
import json
import time


def socket_client():
    client = socket.socket() #定义协议类型,相当于生命socket类型,同时生成socket连接对象
    client.connect(("127.0.0.1", 7777))
    i = 0
    while i < 10:
        msg = {"devIC": "192.168.0.101", "devID": "4c:32:75:8a:ef:a1"}
        #print(type(msg))
        json_str = json.dumps(msg)
        client.send(bytes(json_str, encoding='utf-8'))
        data = client.recv(1024)#这里是字节1k
        print(type(data), data)
        time.sleep(1)
        i += 1
    client.close()


if __name__ == "__main__":

    socket_client()