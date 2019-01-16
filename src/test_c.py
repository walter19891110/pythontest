# -*- coding=utf-8 -*-

from ctypes import *
import os
import time

lib_file = "/iflat/ABE/mycpabe/cpabe-0.11/libmycpabe.so"
libc = cdll.LoadLibrary(lib_file)


def test_abe():
    os.system("cpabe-setup")  # 系统初始化
    os.system("cpabe-keygen pub_key master_key wangjing 'id = 7#4'")  # 生成私钥
    start_time = time.time()
    i = 0
    n = 1
    for i in range(n):  # 循环n次
        os.system("cpabe-enc -k pub_key a.txt 'wangjing and (id > 1#4)'")  # 加密
        # os.system("cpabe-dec -k pub_key priv_key a.txt.cpabe")  # 解密
        i += 1
    use_time = time.time() - start_time
    print("{0} times use time:{1}".format(n, use_time))
    print("avg time:", use_time / n)
    print("times for 1s:{}".format(n / use_time))


def test_mycpabe():
    print(libc.test())

    """初始化生成公钥和主私钥
    cpabe_setup( 
        char* pub_file, 
        char* msk_file 
        )
    """
    setup = libc.cpabe_setup
    setup.argtypes = [c_char_p, c_char_p]
    pub_file = c_char_p(b"/iflat/ABE/mycpabe/pub_key")  # 公钥
    msk_file = c_char_p(b"/iflat/ABE/mycpabe/master_key")  # 主私钥
    setup(pub_file, msk_file)

    """ 生成用户私钥 
    cpabe_keygen( 
        char*  pub_file, 
        char*  msk_file,  
        char*  out_file, 
        char* username, 
        int propertynum, 
        char** userproperty
        )
    """
    prv_key = c_char_p(b"/iflat/ABE/mycpabe/prv_key")  # 待生成的用户私钥名
    username = c_char_p(b"wangjing")  # 用户名
    # 设置用户属性
    property_list = [b"jsyj", b"id = 7#4", b"office = 2362", b"hire_date = 20181121"]  # 用户属性数组
    property_num = c_int(len(property_list))  # 用户属性个数
    # 将list转换称char **
    string_buffers = []
    for i, item in enumerate(property_list):
        cstr = create_string_buffer(len(item) + 1)  # +1是给'\0'留出位置
        cstr.value = item
        string_buffers.append(cstr)
    propertys = (c_char_p * len(property_list))(*map(addressof, string_buffers))  # char**
    # libc.cpabe_keygen(pub_file, msk_file, prv_key, username, property_num, propertys)
    start_time = time.time()
    i = 0
    n = 100
    for i in range(n):  # 循环n次
        libc.cpabe_keygen(pub_file, msk_file, prv_key, username, property_num, propertys)
    use_time = time.time() - start_time
    print("{0} times use time:{1}".format(n, use_time))
    print("avg time:", use_time / n)
    print("times for 1s:{}".format(n / use_time))

    """加密文件
    cpabe_enc( 
        int keep, 
        char* pub_file, 
        char* in_file, 
        char* out_file, 
        char* userpolicy 
        )
    """
    enc = libc.cpabe_enc
    enc.argtypes = [c_int, c_char_p, c_char_p, c_char_p, c_char_p]
    keep = c_int(1)
    in_file = c_char_p(b"/usr/local/ilogsvr/pythontest/src/a.txt")
    out_file = c_char_p(b"/usr/local/ilogsvr/pythontest/src/a1.cpabe")
    policy = c_char_p(b"wangjing and (id > 1#4) and (office = 2362)")  # 访问控制策略
    start_time = time.time()

    for i in range(n):  # 循环n次
        enc(keep, pub_file, in_file, out_file, policy)
    use_time = time.time() - start_time
    print("{0} times use time:{1}".format(n, use_time))
    print("avg time:", use_time / n)
    print("times for 1s:{}".format(n / use_time))

    """解密文件
    cpabe_dec( 
        int keep, 
        char* pub_file, 
        char* prv_file, 
        char* in_file, 
        char* out_file 
        )
    """
    dec = libc.cpabe_dec
    dec.argtypes = [c_int, c_char_p, c_char_p, c_char_p, c_char_p]
    keep = c_int(1)
    my_dec_file = c_char_p(b"/usr/local/ilogsvr/pythontest/src/a2.txt")
    my_in_file = c_char_p(b"/usr/local/ilogsvr/pythontest/src/a1.cpabe")
    start_time = time.time()
    for i in range(n):  # 循环n次
        dec(keep, pub_file, prv_key, my_in_file, my_dec_file)
    use_time = time.time() - start_time
    print("{0} times use time:{1}".format(n, use_time))
    print("avg time:", use_time / n)
    print("times for 1s:{}".format(n / use_time))


if __name__ == "__main__":
    print("test c")
    test_mycpabe()
