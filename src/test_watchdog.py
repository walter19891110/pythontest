
from watchdog.observers import Observer
from watchdog.events import *
import hashlib
import platform
import re
import time
import logging
import logging.config
import requests
from requests_toolbelt import SSLAdapter

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
conf_dir = os.path.join(parent_dir, "conf")

# 初始化日志类
log_conf = os.path.join(conf_dir, "logger.config")
logging.config.fileConfig(log_conf)

# 设置HTTPS
adapter = SSLAdapter('TLSv1.2')  # 设置证书验证方式为TLSv1.2
r = requests.Session()
r.mount('https://', adapter)  # 设置HTTPS的SSL适配器
ca_file = '../certs/chain-ca.pem'  # 设置根证书


class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_moved(self, event):
        if event.is_directory:
            logger = logging.getLogger("root")
            log_str = "directory moved from {0} to {1}".format(event.src_path, event.dest_path)
            # logger.info(log_str)
            # print("directory moved from {0} to {1}".format(event.src_path, event.dest_path))
        else:
            logger = logging.getLogger("root")
            log_str = "file moved from {0} to {1}".format(event.src_path, event.dest_path)
            # logger.info(log_str)
            # print("file moved from {0} to {1}".format(event.src_path, event.dest_path))

    def on_created(self, event):
        if event.is_directory:
            logger = logging.getLogger("root")
            log_str = "directory created:{0}".format(event.src_path)
            # logger.info(log_str)
            # print("directory created:{0}".format(event.src_path))
        else:
            logger = logging.getLogger("root")
            log_str = "file created:{0}".format(event.src_path)
            logger.info(log_str)
            # print("file created:{0}".format(event.src_path))
            analysis_created_file(event.src_path)

    def on_deleted(self, event):
        if event.is_directory:
            logger = logging.getLogger("root")
            log_str = "directory deleted:{0}".format(event.src_path)
            # logger.info(log_str)
            # print("directory deleted:{0}".format(event.src_path))
        else:
            logger = logging.getLogger("root")
            log_str = "file deleted:{0}".format(event.src_path)
            # logger.info(log_str)
            # print("file deleted:{0}".format(event.src_path))

    def on_modified(self, event):
        if event.is_directory:
            logger = logging.getLogger("root")
            log_str = "directory modified:{0}".format(event.src_path)
            # logger.info(log_str)
            # print("directory modified:{0}".format(event.src_path))
        else:
            logger = logging.getLogger("root")
            log_str = "file modified:{0}".format(event.src_path)
            # logger.info(log_str)
            # print("file modified:{0}".format(event.src_path))


def analysis_created_file(file):

    # 获取被创建的文件名
    filename = file.split("/")[-1]
    match_str = r"\.(jar|exe)$"
    if re.search(match_str, filename) is not None:
        print(filename[:-4] + "程序正在安装！")
        # 开始校验可执行文件
        res = verify_md5(file)
        if res["ret_code"] != 0:
            print(filename[:-4], "程序校验失败，禁止安装，删除可执行文件！")
            os.remove(file)


def verify_md5(filename):
    soft_name = filename.split("/")[-1][:-4]  # 获取无后缀的软件名
    os_name = platform.system()
    soft_id = soft_name + "_" + os_name
    soft_md5 = ""
    with open(filename, 'rb') as file:
        data = file.read()
        md5 = hashlib.md5()
        md5.update(data)
        soft_md5 = md5.hexdigest()

    verify_soft_code_api = "https://127.0.0.1:5000/api/soft/verify_soft_code"
    data = {"softID": soft_id, "type": 0, "code": soft_md5}
    r = requests.post(verify_soft_code_api, json=data, verify=ca_file)
    if r.status_code != 200:
        return {"ret_code": r.status_code, "msg": "error"}
    print(r.json())
    return r.json()


if __name__ == "__main__":
    observer = Observer()
    event_handler = FileEventHandler()
    observer.schedule(event_handler, "/Users/walter/Downloads", True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
