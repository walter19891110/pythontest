import sys
from parse.Parse import *
from svc.SoftVersionControl import *
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
import time
import json


client = Client(None)


def init():
    global client
    con_flag = True
    while con_flag:
        try:
            transport = TSocket.TSocket('localhost', 9234)
            transport = TTransport.TBufferedTransport(transport)
            protocol = TBinaryProtocol.TBinaryProtocol(transport)
            client = Client(protocol)
            transport.open()
            con_flag = False
        except Thrift.TException as e:
            # print(e)
            continue


def run():
    print('thrift rpc client start')
    soft_id = "dmdbmon_Darwin"
    verify_type = 0
    verify_code = "e115ec216dc412c0f1d857fcf6e9202b"
    j = 0
    while j < 1:
        j += 1
        i = 0
        time_start = time.time()
        while i < 1:
            # res = client.get_soft_list()
            # res = client.verify_soft_code(soft_id, verify_type, verify_code)
            res = client.get_soft_info(soft_id)
            dic = json.loads(res)
            print(dic["softinfo"])
            i = i + 1
        time_end = time.time()
        print('thrift rpc use time', time_end - time_start)


if __name__ == '__main__':
    init()
    run()
