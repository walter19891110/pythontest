import sys
from parse.Parse import *
from parse.ttypes import *
from thrift.Thrift import TType, TMessageType, TException
from thrift.Thrift import TProcessor
from thrift.transport import TSocket
from thrift.protocol import TBinaryProtocol, TProtocol
from thrift.server import TServer
import logging
from parse.constants import *
import json


class ParseHandler:
    """
    真正的服务代码。
    类名为hrift中定义的服务名+Handler
    函数名、参数等要与thrift中服务名下定义的接口一致
    """
    def parse2json(self, str):
        print("start parse str")
        json_str = {"server": str}
        return json.dumps(json_str)


def run():
    """服务运行代码"""
    # 创建服务端
    handler = ParseHandler()
    processor = Processor(handler)

    # 监听端口
    transport = TSocket.TServerSocket('localhost', 9234)

    # 选择传输层
    tfactory = TTransport.TBufferedTransportFactory()

    # 选择传输协议
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    # 创建服务端
    server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)
    server.setNumThreads(5)

    print('start thrift serve in python')
    server.serve()
    print('done!')


if __name__ == '__main__':
    run()


