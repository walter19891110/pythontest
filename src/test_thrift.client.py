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


def add_soft():
    global client
    soft_dict = SoftInfoDict(
        softid="Solarized_Darwin",
        softname="Solarized",
        osname="Darwin",
        softmode=0,
        setupname="Solarized",
        setupcode="df6a62b5ca3d2e833b49e803ff99f59a",
        mainfile="Solarized",
        maincode="df6a62b5ca3d2e833b49e803ff99f59a",
        desc="Solarized")
    res = client.add_soft_info(soft_dict)
    result = json.loads(res)
    print(result)


def run():
    global client
    print('thrift rpc client start')
    soft_id = "dmdbmon_Darwin"
    soft_mode = 0
    verify_type = 0
    verify_code = "1"
    j = 0
    while j < 1:
        j += 1
        i = 0
        time_start = time.time()
        while i < 1:
            # res = client.get_soft_list()
            # res = client.verify_soft_code(soft_id, verify_type, verify_code)
            # res = client.get_soft_info(soft_id)
            # res = client.modify_soft_mode(soft_id, soft_mode)
            # res = client.add_soft_code(soft_id, verify_type, verify_code)
            res = client.del_soft_code(soft_id, verify_type, verify_code)
            dic = json.loads(res)
            print(dic)
            res = client.get_soft_info(soft_id)
            dic = json.loads(res)
            print(dic)
            i = i + 1
        time_end = time.time()
        print('thrift rpc use time', time_end - time_start)


if __name__ == '__main__':
    init()
    run()
    # add_soft()
