import psutil
import hashlib
import platform
import re


def test_com():

    print(psutil.cpu_count())  # 逻辑CPU数
    print(psutil.cpu_count(logical=False))  # 物理CPU数
    print(psutil.cpu_times())  # 统计CPU的用户／系统／空闲时间
    print(psutil.cpu_percent(interval=1, percpu=True))  # CPU使用率，每秒刷新一次
    print(psutil.test())  # 模拟ps命令


def test_pro():
    # print(psutil.pids())  # 所有进程ID
    pids = psutil.pids()
    for i in pids:
        get_pro_info(i)


def get_pro_info(pid):
    """根据进程ID获取进程信息

    :param pid: 进程ID
    :return:
    """

    p = psutil.Process(pid)  # 获取指定进程的进程信息

    filename = p.exe()  # 进程可执行文件的路径
    # print(filename)
    # get_md5(filename)  # 计算可执行文件的MD5

    # 打印进程信息
    user = p.username()
    pro_name = p.name()
    if user == "walter":
        if pro_name == "java":
            print("进程名称:", p.name(), pid)  # 进程名称
            print("进程exe路径:", p.exe())  # 进程exe路径
            # print("进程工作目录:", p.cwd())  # 进程工作目录
            print("进程启动的命令行:", p.cmdline())  # 进程启动的命令行
            cmd_str = p.cmdline()[2]  # 获取jar文件路径
            jar_str = cmd_str.split("/")[-1]  # 获取jar文件名
            match_str = r"\.jar$"
            if re.search(match_str, jar_str) is not None:
                # 是jar文件，获取该文件的绝对路径
                if cmd_str[0] == "/":  # 路径第一个字符是'/'，说明是使用的绝对路径
                    get_md5(cmd_str)  # 计算MD5
                    # -----校验MD5----- #
                    # -----校验MD5----- #
                else:  # 不是绝对路径。和工作目录一起，拼接出绝对路径
                    cmd_str = p.cwd() + "/" + cmd_str
                    get_md5(cmd_str)  # 计算MD5
                    # -----校验MD5----- #
                    # -----校验MD5----- #
            else:
                # 不是使用jar文件启动的，如ES、spark、hadoop等，挨个排查系统中部署的此类软件
                cmd_str = " ".join(p.cmdline())
                # print(cmd_str)
                # -------读取常用非jar文件运行的软件列表------ #
                not_jar_list = ["elasticsearch", "spark"]  # 正式程序中需从配置文件中读取
                flag = 0
                for i in not_jar_list:
                    match_str = i
                    if re.search(match_str, cmd_str) is not None:
                        flag = 1
                        print(match_str + "不需进行版本控制!")
                        break
                if flag == 0:
                    # 不在列表中，说明是非法运行的程序，需进行告警
                    print("非法程序", cmd_str)

            print("\n")
        elif pro_name == "Python":
            print("进程名称:", p.name(), pid)  # 进程名称
            # print("进程exe路径:", p.exe())  # 进程exe路径
            # print("进程工作目录:", p.cwd())  # 进程工作目录
            # print("进程启动的命令行:", p.cmdline())  # 进程启动的命令行
            cmd_str = p.cmdline()[1]
            if cmd_str[0] == "/":  # 路径第一个字符是'/'，说明是使用的绝对路径
                get_md5(cmd_str)  # 计算MD5
                # -----校验MD5----- #
                # -----校验MD5----- #
            else:  # 不是绝对路径。和工作目录一起，拼接出绝对路径
                cmd_str = p.cwd() + "/" + cmd_str
                get_md5(cmd_str)  # 计算MD5
                # -----校验MD5----- #
                # -----校验MD5----- #
            print("\n")
        else:
            # c语言程序直接使用p.exe()，即可找到主程序文件
            # pass
            print("进程名称:", p.name(), pid)  # 进程名称
            # print("进程exe路径:", p.exe())  # 进程exe路径
            # print("进程工作目录:", p.cwd())  # 进程工作目录
            # print("进程启动的命令行:", p.cmdline())  # 进程启动的命令行
            # print("\n")

        """
        print("进程用户名:", p.username())  # 进程用户名
        print("父进程ID:", p.ppid())  #父进程ID
        print("父进程:", p.parent())  # 父进程
        print("子进程列表:", p.children())  # 子进程列表

        print("进程状态:", p.status())  # 进程状态
        print("进程用户名:", p.username())  # 进程用户名
        print("进程创建时间:", p.create_time())  # 进程创建时间
        print("进程终端:", p.terminal())  # 进程终端

        print("进程使用的CPU时间:", p.cpu_times())  # 进程使用的CPU时间
        print("进程使用的内存:", p.memory_info())  # 进程使用的内存
        print("进程打开的文件:", p.open_files())  # 进程打开的文件
        print("进程相关网络连接:", p.connections())  # 进程相关网络连接

        print("进程的线程数量:", p.num_threads())  # 进程的线程数量
        # print("所有线程信息:", p.threads())  # 所有线程信息
        print("进程环境变量:", p.environ())  # 进程环境变量
        # p.terminate()  # 结束进程
        """
        # print("\n")


def get_md5(filename):
    pro_md5 = hashlib.md5()
    with open(filename, 'rb') as file:
        data = file.read()
        pro_md5.update(data)
        print(filename + "的MD5值：", pro_md5.hexdigest())
    return pro_md5.hexdigest()


def soft_run_control(user_list):
    pids = psutil.pids()
    for pid in pids:
        p = psutil.Process(pid)  # 获取指定进程的进程信息
        if p.username() in user_list:
            soft_run_info(p)


def soft_run_info(p):
    if p.name() == "java":  # Java程序
        print("进程启动的命令行:", p.cmdline())  # 进程启动的命令行
        cmd_str = p.cmdline()[2]  # 获取jar文件路径
        jar_str = cmd_str.split("/")[-1]  # 获取jar文件名
        match_str = r"\.jar$"
        if re.search(match_str, jar_str) is not None:
            # 是jar文件，获取该文件的绝对路径
            if cmd_str[0] != "/":  # 路径第一个字符不是'/'，说明不是使用的绝对路径
                cmd_str = p.cwd() + "/" + cmd_str  # 和工作目录一起，拼接出绝对路径

            verify_md5(cmd_str)
        else:
            # 不是使用jar文件启动的，如ES、spark、hadoop等，挨个排查系统中部署的此类软件
            cmd_str = " ".join(p.cmdline())
            # print(cmd_str)
            # -------读取常用非jar文件运行的软件列表------ #
            not_control_list = ["elasticsearch", "spark"]  # 正式程序中需从配置文件中读取
            illegal = True  # 是否为非法启动
            for match_str in not_control_list:
                if re.search(match_str, cmd_str) is not None:
                    illegal = False
                    print(match_str + "不需进行版本控制!")
                    break
            if illegal:
                # 不在列表中，说明是非法运行的程序，需进行告警
                # -----生成告警-------- #
                print("非法程序, 启动命令为", cmd_str)
                # -----生成告警-------- #

        print("\n")
    elif p.name() == "Python":
        print("进程启动的命令行:", p.cmdline())  # 进程启动的命令行
        cmd_str = p.cmdline()[1]
        if cmd_str[0] != "/":  # 路径第一个字符不是'/'，说明不是使用的绝对路径
            cmd_str = p.cwd() + "/" + cmd_str  # 和工作目录一起，拼接出绝对路径

        verify_md5(cmd_str)
        print("\n")
    else:
        # c语言程序直接使用p.exe()，即可找到主程序文件
        verify_md5(p.exe())


def verify_md5(filename):
    soft_name = filename.split("/")[-1]
    os_name = platform.system()
    soft_id = soft_name + "_" + os_name
    soft_md5 = ""
    with open(filename, 'rb') as file:
        data = file.read()
        md5 = hashlib.md5()
        md5.update(data)
        soft_md5 = md5.hexdigest()
    # print(soft_id, soft_md5)
    # -----校验MD5----- #
    # print("向服务端请求校验MD5值")
    # -----校验MD5----- #


if __name__ == "__main__":

    os = platform.system()
    print("操作系统为", os)
    # test_pro()
    user_list = ["walter"]
    soft_run_control(user_list)




