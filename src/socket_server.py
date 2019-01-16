import socketserver
import time
import json
import requests
from requests_toolbelt import SSLAdapter


class MyServer(socketserver.BaseRequestHandler):

    def handle(self):
        # print("1")
        # print("from conn:", self.request)
        conn = self.request  # 每个客户端的连接
        # print(self.client_address)
        # conn.sendall(b"conn success!")  # 回复客户端连接已建立
        while True:
            recv = conn.recv(1024)
            if len(recv) <= 0:
                break
            json_data = str(recv, encoding='utf-8')
            data = json.loads(json_data)
            # print(type(data), data)

            # 设置HTTPS
            adapter = SSLAdapter('TLSv1.2')  # 设置证书验证方式为TLSv1.2
            r = requests.Session()
            r.mount('https://', adapter)  # 设置HTTPS的SSL适配器
            ca_file = '../certs/chain-ca.pem'  # 设置根证书

            # 终端入网验证
            dev_verify_api = 'https://127.0.0.1:5000/api/dev/dev_verify'
            r = requests.post(dev_verify_api, json=data, verify=ca_file)  # 指定根证书
            # print(r.json())
            json_str = json.dumps(r.json())
            conn.sendall(bytes(json_str, encoding='utf-8'))

    def finish(self):
        print("客户端:", self.client_address, "的连接已断开!")


def dap_server():
    s1 = socketserver.ThreadingTCPServer(("127.0.0.1", 7777), MyServer)  # 多线程
    s1.serve_forever()


if __name__ == "__main__":
    dap_server()
    print("hello")
