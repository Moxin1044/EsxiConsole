import argparse
import json
import ipaddress

from api import *

# 输入输出的特殊调用
from termcolor import colored
import getpass
from tabulate import tabulate

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

    if args.command == 'login':
        login_ec()

    if args.command == 'set':
        set_ec()


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
        message = colored('* [Success]: 您成功的与Esxi服务器建立连接', 'green')
    else:
        message = colored('* [Errors]: 您无法与Esxi服务器建立连接', 'red')
    print(message)


def info_ec():
    esxi_host = get_configs()['EsxiAddr']
    esxi_user = get_configs()['EsxiUser']
    message = colored('* [INFO]: \n* Esxi HOST: ' + esxi_host + '\n* Esxi User: ' + esxi_user, 'blue')
    print(message)


def login_ec():
    print(colored('* [Warning]: 请确保你的输入环境是安全的！这将保护你的ESXI服务器！', 'yellow'))
    print(colored('* [Warning]: 为了确保您的安全，输入密码不显示是正常的哦！', 'yellow'))
    username = input("请输入ESXI用户名：")
    password = getpass.getpass("请输入ESXI密码：")
    # 打开并读取JSON文件
    with open('ec_config.json', 'r') as f:
        data = json.load(f)

    # 更新节点的值
    data['EsxiUser'] = username
    data['EsxiPass'] = password

    # 将更新后的Python字典转换回JSON格式
    with open('ec_config.json', 'w') as f:
        json.dump(data, f)
    print(colored('* [Success]: 已成功更新用户名和密码', 'green'))
    print(colored('* [INFO]: 即将验证用户名和密码', 'blue'))
    check_ec()


def set_ec():
    print(colored('* [Warning]: 您正在设置的是Esxi的服务器地址，请正确填写，否则会导致失败。', 'yellow'))
    print(colored('* [Warning]: 直接输入IP地址即可。', 'yellow'))
    ip = input("请输入ESXI的IP：")
    # 打开并读取JSON文件
    with open('ec_config.json', 'r') as f:
        data = json.load(f)

    if is_valid_ip(ip):
        # 更新节点的值
        data['EsxiAddr'] = ip

        # 将更新后的Python字典转换回JSON格式
        with open('ec_config.json', 'w') as f:
            json.dump(data, f)
        print(colored('* [Success]: 已成功更新用户名和密码', 'green'))
    else:
        print(colored('* [Errors]: IP地址验证错误！', 'red'))


def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


if __name__ == '__main__':
    main()
