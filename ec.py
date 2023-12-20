import argparse
from tabulate import tabulate

from api import *


def main():
    parser = argparse.ArgumentParser(description='一个简单的Python脚本，演示如何使用命令行参数。')

    # 添加位置参数
    parser.add_argument('command', help='指定命令（例如：list）')

    args = parser.parse_args()

    # 处理参数
    if args.command == 'list':
        list_ec()


def list_ec():
    ec_list = get_all_esxi_machines()
    table = tabulate(ec_list, headers="keys", tablefmt="pretty")
    print(table)


if __name__ == '__main__':
    main()
