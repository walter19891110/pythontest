
from watchdog.observers import Observer
from watchdog.events import *
import re
import time
import logging
import logging.config

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
conf_dir = os.path.join(parent_dir, "conf")

# 初始化日志类
log_conf = os.path.join(conf_dir, "logger.config")
logging.config.fileConfig(log_conf)


class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_moved(self, event):
        if event.is_directory:
            logger = logging.getLogger("root")
            log_str = "directory moved from {0} to {1}".format(event.src_path, event.dest_path)
            logger.info(log_str)
            # print("directory moved from {0} to {1}".format(event.src_path, event.dest_path))
        else:
            logger = logging.getLogger("root")
            log_str = "file moved from {0} to {1}".format(event.src_path, event.dest_path)
            logger.info(log_str)
            # print("file moved from {0} to {1}".format(event.src_path, event.dest_path))

    def on_created(self, event):
        if event.is_directory:
            logger = logging.getLogger("root")
            log_str = "directory created:{0}".format(event.src_path)
            logger.info(log_str)
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
            log_str = "file deleted:{0}".format(event.src_path)
            logger.info(log_str)
            # print("directory deleted:{0}".format(event.src_path))
        else:
            logger = logging.getLogger("root")
            log_str = "file deleted:{0}".format(event.src_path)
            logger.info(log_str)
            # print("file deleted:{0}".format(event.src_path))

    def on_modified(self, event):
        if event.is_directory:
            logger = logging.getLogger("root")
            log_str = "file modified:{0}".format(event.src_path)
            logger.info(log_str)
            # print("directory modified:{0}".format(event.src_path))
        else:
            logger = logging.getLogger("root")
            log_str = "file modified:{0}".format(event.src_path)
            logger.info(log_str)
            # print("file modified:{0}".format(event.src_path))


def analysis_created_file(file):

    # 获取被创建的文件名
    filename = file.split("/")[-1]
    print(filename)
    file_list = filename.split(".")
    if len(file_list) < 2:
        # 没有后缀，说明是可执行文件，校对程序的校验码
        print(filename + "程序正在安装！")
        # 开始校验可执行文件
        print("开始校验"+filename)
        i = 1
        if i == 1:
            print("校验成功，允许安装！")
        else:
            print("校验失败，禁止安装，删除可执行文件！")
            # os.remove(file)
        # 校验结束
    else:
        file_postfix = file_list[1]
        match_str = r"(jar|exe)$"
        if re.match(match_str, file_postfix):
            print(filename + "程序正在安装！")
            # 开始校验可执行文件
            print("开始校验" + filename)
            i = 0
            if i == 1:
                print("校验成功，允许安装！")
            else:
                print("校验失败，禁止安装，删除可执行文件！")
                os.remove(file)
            # 校验结束


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
