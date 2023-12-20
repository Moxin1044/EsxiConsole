import argparse
from tabulate import tabulate

from api import *

from termcolor import colored

from modules import get_configs, append_info_log, append_error_log, append_warning_log


def main():
    parser = argparse.ArgumentParser(description='一个简单的Python脚本，演示如何使用命令行参数。')

    # 添加位置参数
    parser.add_argument('command', help='指定命令（例如：list help）')

    args = parser.parse_args()

    # 处理参数
    if args.command == 'list':
        list_ec()

    if args.command == 'help':
        help_ec()

    if args.command == 'check':
        check_ec()

    if args.command == 'info':
        info_ec()


def list_ec():
    ec_list = get_all_esxi_machines()
    table = tabulate(ec_list, headers="keys", tablefmt="pretty")
    print(table)


def help_ec():
    text = """帮助：
    命令格式： ec.py [command]
    list   查看Esxi中虚拟机列表
    help   呼出当前帮助
    check  检查当前是否能正常连接ESXI服务器
    info   检查当前连接的服务器信息
    set    设置Esxi Host
    login  登录Esxi
    """
    print(text)


def check_ec():
    if check_esxi_host():
        message = f"{colored('* [Success]:', 'green')} {colored('您成功的与Esxi服务器建立连接！', 'blue')}"
    else:
        message = f"{colored('* [Errors]:', 'red')} {colored('您无法与Esxi服务器建立连接！', 'yellow')}"
    print(message)


def info_ec():
    esxi_host = get_configs()['EsxiAddr']
    esxi_user = get_configs()['EsxiUser']
    message = colored('* [INFO]: \n* Esxi HOST: ' + esxi_host + '\n* Esxi User: ' + esxi_user, 'blue')
    print(message)


def login_ec():
    print(colored('* [Warning]: 请确保你的输入环境是安全的！这将保护你的ESXI服务器！', 'yellow'))
    username = input("请输入用户名：")



if __name__ == '__main__':
    main()
