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

    if args.command == 'look':
        look_ec()

    if args.command == 'off':
        off_ec()

    if args.command == 'reboot':
        reboot_ec()

    if args.command == 'shutdown':
        look_ec()

    if args.command == 'on':
        on_ec()

    if args.command == 'reset':
        reset_ec()

    if args.command == 'suspend':
        suspend_ec()

    if args.command == 'standby':
        standby_ec()

    if args.command == 'destroy':
        destroy_ec()

    if args.command == 'rename':
        rename_ec()

    if args.command == 'cs':
        look_ec()

    if args.command == 'ds':
        look_ec()

    if args.command == 'rs':
        look_ec()

    if args.command == 'log':
        look_ec()


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
    look      查看指定虚拟机的截图
    off       关闭指定的虚拟机
    reboot    重启指定的虚拟机
    shutdown  关机指定的虚拟机
    on        开启指定的虚拟机
    reset     重置指定的虚拟机
    suspend   挂起指定的虚拟机
    standby   休眠指定的虚拟机
    destroy   销毁指定的虚拟机
    rename    改名指定的虚拟机
    ls     列出指定虚拟机的快照
    cs     拍摄指定虚拟机的快照
    ds     删除指定虚拟机的快照
    rs     恢复指定虚拟机的快照
    log       输出日志
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
    print(colored('* [INFO]: 直接输入IP地址即可。', 'blue'))
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


def look_ec():
    name = input("输入虚拟机名称：")
    look = get_esxi_machines_screenshot(name)
    if look:
        print(colored('* [Success]: 已成功获取虚拟机截图。', 'green'))
        print(colored(f'* [Success]: 保存地址为 {look}。', 'green'))
    else:
        print(colored('* [Errors]: 无法获取到虚拟机截图，请查看日志确认错误！', 'red'))


def off_ec():
    name = input("输入虚拟机名称：")
    look = poweroff_esxi_machines(name)
    if look:
        print(colored('* [Success]: 已成功关闭虚拟机电源。', 'green'))
    else:
        print(colored('* [Errors]: 无法关闭该机器，请查看日志确认错误！', 'red'))


def reboot_ec():
    name = input("输入虚拟机名称：")
    look = reboot_esxi_machines(name)
    if look:
        print(colored('* [Success]: 已成功重启虚拟机。', 'green'))
    else:
        print(colored('* [Errors]: 无法重启该机器，请查看日志确认错误！', 'red'))


def shutdown_ec():
    name = input("输入虚拟机名称：")
    look = shutdown_esxi_machines(name)
    if look:
        print(colored('* [Success]: 已成功关机虚拟机。', 'green'))
    else:
        print(colored('* [Errors]: 无法关机该机器，请查看日志确认错误！', 'red'))


def on_ec():
    name = input("输入虚拟机名称：")
    look = poweron_esxi_machines(name)
    if look:
        print(colored('* [Success]: 已成功开启虚拟机。', 'green'))
    else:
        print(colored('* [Errors]: 无法开启该机器，请查看日志确认错误！', 'red'))


def reset_ec():
    name = input("输入虚拟机名称：")
    look = reset_esxi_machines(name)
    if look:
        print(colored('* [Success]: 已成功重置虚拟机。', 'green'))
    else:
        print(colored('* [Errors]: 无法重置该机器，请查看日志确认错误！', 'red'))


def suspend_ec():
    name = input("输入虚拟机名称：")
    look = reset_esxi_machines(name)
    if look:
        print(colored('* [Success]: 已成功挂起虚拟机。', 'green'))
    else:
        print(colored('* [Errors]: 无法挂起该机器，请查看日志确认错误！', 'red'))


def standby_ec():
    name = input("输入虚拟机名称：")
    look = standby_esxi_machines(name)
    if look:
        print(colored('* [Success]: 已成功休眠虚拟机。', 'green'))
    else:
        print(colored('* [Errors]: 无法休眠该机器，请查看日志确认错误！', 'red'))


def destroy_ec():
    name = input("输入虚拟机名称：")
    look = destroy_esxi_machines(name)
    if look:
        print(colored('* [Success]: 已成功销毁虚拟机。', 'green'))
    else:
        print(colored('* [Errors]: 无法销毁该机器，请查看日志确认错误！', 'red'))


def rename_ec():
    name = input("输入虚拟机名称：")
    new_name = input("输入新的虚拟机名称：")
    look = rename_esxi_machines(name, new_name)
    if look:
        print(colored('* [Success]: 已成功重命名虚拟机。', 'green'))
    else:
        print(colored('* [Errors]: 无法重命名该机器，请查看日志确认错误！', 'red'))


if __name__ == '__main__':
    main()
