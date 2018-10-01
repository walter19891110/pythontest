import time
import requests
from requests_toolbelt import SSLAdapter


def performance_test():
    # 设置HTTPS
    adapter = SSLAdapter('TLSv1.2')  # 设置证书验证方式为TLSv1.2
    r = requests.Session()
    r.mount('https://', adapter)  # 设置HTTPS的SSL适配器
    ca_file = '../certs/chain-ca.pem'  # 设置根证书
    while True:
        i = 0
        time_start = time.time()
        while i < 10:
            id_verify_api = 'https://127.0.0.1:5000/api/auth/id_verify'
            data = {"username": "wangjing", "type": 1, "data": "wangjing"}
            #r = requests.post(id_verify_api, json=data, verify=ca_file)
            r = requests.post(id_verify_api, json=data, verify=ca_file)
            i = i+1
        time_end = time.time()
        print('use time', time_end - time_start)


def test():
    # 设置HTTPS
    adapter = SSLAdapter('TLSv1.2')  # 设置证书验证方式为TLSv1.2
    r = requests.Session()
    r.mount('https://', adapter)  # 设置HTTPS的SSL适配器
    ca_file = '../certs/chain-ca.pem'  # 设置根证书
    while True:
        i = 0
        time_start = time.time()
        while i < 100000:
            test_api = 'https://127.0.0.1:5000/api/test'
            data = {"a": 1, "b": 2}
            #r = requests.post(test_api, json=data)
            r = requests.post(test_api, json=data, verify=ca_file)
            i = i+1
        time_end = time.time()
        print('use time', time_end - time_start)


def test_dev_verify_noredis():

    ca_file = '../certs/chain-ca.pem'  # 设置根证书
    while True:
        i = 0
        time_start = time.time()
        while i < 10000:
            dev_verify_api = 'https://127.0.0.1:5000/api/dev/dev_verify_noredis'
            data = {'devID': "93e50ecb50de1f04af1252075f829661", 'devIC': "a541dddab6cb3ad680053f55559ad394"}
            #r = requests.post(id_verify_api, json=data, verify=ca_file)
            r = requests.post(dev_verify_api, json=data, verify=ca_file)
            i = i+1
        time_end = time.time()
        print('use time', time_end - time_start)

if __name__ == "__main__":

    performance_test()
    print('hello')
    #test()
    #test_dev_verify_noredis()