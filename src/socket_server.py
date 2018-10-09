import socketserver
import time


class MyServer(socketserver.BaseRequestHandler):

    def handle(self):
        # print("1")
        # print("from conn:", self.request)
        conn = self.request  # 每个客户端的连接
        conn.sendall(b"conn success!")  # 回复客户端连接已建立
        while True:
            print(conn.recv(1024))
            time.sleep(1)
        # self.request.send("1")
        # data = self.request.recv(1024).strip()  # 每一个请求都会实例化MyTCPHandler(socketserver.BaseRequestHandler):
        # print("{} wrote:".format(self.client_address[0]))
        # print(data)

    def finish(self):

        print("连接已断开!")


if __name__ == "__main__":
    s1=socketserver.ThreadingTCPServer(("127.0.0.1", 7777), MyServer)
    s1.serve_forever()
