import ssl
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim

import requests, os
import urllib3
from requests.auth import HTTPBasicAuth

from modules import get_configs, append_info_log, append_error_log, append_warning_log

# 禁用 SSL 证书验证
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# 替换为你的 ESXi 主机的 IP 地址、用户名和密码
esxi_host = get_configs()['EsxiAddr']
esxi_user = get_configs()['EsxiUser']
esxi_password = get_configs()['EsxiPass']


def check_esxi_host():
    try:
        si = SmartConnect(host=esxi_host, user=esxi_user, pwd=esxi_password, port=443, sslContext=ssl_context)
        content = si.RetrieveContent()
        Disconnect(si)
        if content:
            return True
        return False
    except:
        return False


def get_all_esxi_machines():
    # 连接到 ESXi 主机

    si = SmartConnect(host=esxi_host, user=esxi_user, pwd=esxi_password, port=443, sslContext=ssl_context)

    # 获取虚拟机列表
    content = si.RetrieveContent()
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    vms = vm_view.view
    # 遍历虚拟机列表
    data = []
    i = 0
    for vm in vms:
        # 获取磁盘大小
        virtual_disks = [device for device in vm.config.hardware.device if
                         isinstance(device, vim.vm.device.VirtualDisk)]
        disk_capacity_bytes = 0
        for disk in virtual_disks:
            disk_capacity_bytes += disk.capacityInBytes
        disk_capacity_bytes = disk_capacity_bytes / (1024**3)
        # 获取磁盘大小结束 单位 Bytes
        # 打印虚拟机名称和状态
        i += 1
        data.append({"Name": vm.name, "PowerState": vm.runtime.powerState, "Memory(MB)": vm.config.hardware.memoryMB, "CPU(num)": vm.config.hardware.numCPU, "Disk(GB)": disk_capacity_bytes, "Paused": vm.runtime.paused, "IpAddress": vm.guest.ipAddress, "HostName": vm.guest.hostName, "OsName": vm.config.guestFullName})
    # 断开连接
    Disconnect(si)
    append_info_log(f"获取ESXI中虚拟机列表：{data}")
    return data


def get_esxi_machines_screenshot(vm_name):
    # 连接到 ESXi 主机
    si = SmartConnect(host=esxi_host, user=esxi_user, pwd=esxi_password, port=443, sslContext=ssl_context)

    # 获取虚拟机列表
    content = si.RetrieveContent()
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    vms = vm_view.view

    # 查找要获取截图的虚拟机
    target_vm = None
    for vm in vms:
        if vm.name == vm_name:
            target_vm = vm
            break

    # 获取虚拟机屏幕截图
    if target_vm:
        # 禁用证书验证
        urllib3.disable_warnings()
        screenshot_url = f'https://{esxi_host}:443/screen?id={target_vm._moId}'
        append_info_log(f"获取ID：{target_vm._moId}({vm_name})的虚拟机截图")
        auth = HTTPBasicAuth(esxi_user, esxi_password)
        response = requests.get(screenshot_url, verify=False, auth=auth)
        Disconnect(si)
        if response.status_code == 200:
            add = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/log/screenhost/' + str(target_vm._moId) + 'screenshot.png'
            with open(add, 'wb') as file:
                file.write(response.content)
            append_info_log(f"成功获取ID：{target_vm._moId}({vm_name})的虚拟机截图：{add}")
            return add
        else:
            append_error_log(f"无法获取ID：{target_vm._moId}({vm_name})的虚拟机截图：可能无法连接服务。状态码：{response.status_code}")
            return False
    else:
        append_warning_log(f"无法获取 {vm_name} 的虚拟机截图：无法找到/不存在该虚拟机。")
        return False


# 快照递归 用于 get_esxi_machines_snapshots 一般不调用
def list_snapshots(snapshot_tree, snap_list=None):
    if snap_list is None:
        snap_list = []
    for snapshot in snapshot_tree:
        snap_list.append({"name": snapshot.name, "description": snapshot.description, "createTime": f"{snapshot.createTime}"})
        # 如果存在子快照，递归调用该函数
        if snapshot.childSnapshotList:
            list_snapshots(snapshot.childSnapshotList, snap_list)
        return snap_list


# 列出快照
def get_esxi_machines_snapshots(vm_name):
    si = SmartConnect(host=esxi_host, user=esxi_user, pwd=esxi_password, port=443, sslContext=ssl_context)

    # 获取虚拟机列表
    content = si.RetrieveContent()

    # 获取虚拟机对象
    vm = None
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)

    for obj in container.view:
        if obj.name == vm_name:
            vm = obj
            break

    if vm is None:
        append_warning_log(f"未找到名为 {vm_name} 的虚拟机")
        return False

    snapshots = vm.snapshot.rootSnapshotList
    if not snapshots:
        append_info_log(f"没有找到虚拟机 {vm_name} 的快照")
    else:
        list = list_snapshots(snapshots)
        return append_info_log(f"找到虚拟机 {vm_name} 的快照：{list}")

