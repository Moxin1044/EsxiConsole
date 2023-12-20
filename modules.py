import datetime
import json
import os


def get_configs():
    with open(os.path.dirname(os.path.abspath(__file__)) + "/ec_config.json", 'r') as file:
        data = json.load(file)
        return data


def append_info_log(data):
    # 获取当前时间并格式化为指定格式
    current_time = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

    # 构建日志信息
    log_entry = f"{current_time} |INFO| {data}\n"

    # 将日志信息追加到文件
    with open(os.path.dirname(os.path.abspath(__file__)) + "/log/logs.txt", 'a') as log_file:
        log_file.write(log_entry)


def append_error_log(data):
    # 获取当前时间并格式化为指定格式
    current_time = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

    # 构建日志信息
    log_entry = f"{current_time} |ERROR| {data}\n"

    # 将日志信息追加到文件
    with open(os.path.dirname(os.path.abspath(__file__)) + "/log/logs.txt", 'a') as log_file:
        log_file.write(log_entry)


def append_warning_log(data):
    # 获取当前时间并格式化为指定格式
    current_time = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

    # 构建日志信息
    log_entry = f"{current_time} |WARNING| {data}\n"

    # 将日志信息追加到文件
    with open(os.path.dirname(os.path.abspath(__file__)) + "/log/logs.txt", 'a') as log_file:
        log_file.write(log_entry)
