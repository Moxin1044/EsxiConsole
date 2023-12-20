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

# 检查 ESXi 主机是否可达
def check_esxi_host():
    # 尝试连接 ESXi 主机
    si = SmartConnect(host=esxi_host, user=esxi_user, pwd=esxi_password, port=443, sslContext=ssl_context)
    content = si.RetrieveContent()
    Disconnect(si)
    # 如果成功连接，返回 True；否则，返回 False
    if content:
        return True
    return False

# 获取所有 ESXi 主机上虚拟机的信息
def get_all_esxi_machines():
    # 连接 ESXi 主机
    si = SmartConnect(host=esxi_host, user=esxi_user, pwd=esxi_password, port=443, sslContext=ssl_context)
    content = si.RetrieveContent()
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    vms = vm_view.view
    data = {}
    i = 0
    for vm in vms:
        # 获取磁盘大小
        virtual_disks = [device for device in vm.config.hardware.device if isinstance(device, vim.vm.device.VirtualDisk)]
        disk_capacity_bytes = sum(disk.capacityInBytes for disk in virtual_disks)
        # 收集虚拟机信息
        i += 1
        data.update({
            str(i): {
                "Name": vm.name,
                "powerState": vm.runtime.powerState,
                "memoryMB": vm.config.hardware.memoryMB,
                "numCPU": vm.config.hardware.numCPU,
                "capacityInBytes": disk_capacity_bytes,
                "paused": vm.runtime.paused,
                "ipAddress": vm.guest.ipAddress,
                "hostName": vm.guest.hostName,
                "guestFullName": vm.config.guestFullName
            }
        })
    # 断开连接
    Disconnect(si)
    # 记录获取的虚拟机信息
    append_info_log(f"ESXi 虚拟机列表：{data}")
    return data

# 获取特定虚拟机在 ESXi 主机上的屏幕截图
def get_esxi_machines_screenshot(vm_name):
    # 连接 ESXi 主机
    si = SmartConnect(host=esxi_host, user=esxi_user, pwd=esxi_password, port=443, sslContext=ssl_context)
    content = si.RetrieveContent()
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    vms = vm_view.view
    target_vm = None
    for vm in vms:
        if vm.name == vm_name:
            target_vm = vm
            break
    if target_vm:
        # 禁用证书验证
        urllib3.disable_warnings()
        screenshot_url = f'https://{esxi_host}:443/screen?id={target_vm._moId}'
        # 记录获取截图的日志
        append_info_log(f"获取 ID：{target_vm._moId}（{vm_name}）的虚拟机截图")
        auth = HTTPBasicAuth(esxi_user, esxi_password)
        response = requests.get(screenshot_url, verify=False, auth=auth)
        # 断开连接
        Disconnect(si)
        if response.status_code == 200:
            # 保存截图
            add = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'log', 'screenhost', f'{target_vm._moId}screenshot.png')
            with open(add, 'wb') as file:
                file.write(response.content)
            # 记录成功获取截图的日志
            append_info_log(f"成功获取 ID：{target_vm._moId}（{vm_name}）的虚拟机截图：{add}")
            return add
        else:
            # 记录无法获取截图的错误日志
            append_error_log(f"无法获取 ID：{target_vm._moId}（{vm_name}）的虚拟机截图：可能无法连接服务。状态码：{response.status_code}")
            return False
    else:
        # 记录无法获取截图的警告日志
        append_warning_log(f"无法获取 {vm_name} 的虚拟机截图：无法找到/不存在该虚拟机。")
        return False

# 用于列出快照的递归函数
def list_snapshots(snapshot_tree, snap_list=None):
    if snap_list is None:
        snap_list = []
    for snapshot in snapshot_tree:
        # 添加快照信息到列表
        snap_list.append({
            "name": snapshot.name,
            "description": snapshot.description,
            "createTime": f"{snapshot.createTime}"
        })
        # 如果存在子快照，递归调用该函数
        if snapshot.childSnapshotList:
            list_snapshots(snapshot.childSnapshotList, snap_list)
    return snap_list

# 列出特定虚拟机在 ESXi 主机上的快照
def get_esxi_machines_snapshots(vm_name):
    # 连接 ESXi 主机
    si = SmartConnect(host=esxi_host, user=esxi_user, pwd=esxi_password, port=443, sslContext=ssl_context)
    content = si.RetrieveContent()
    # 获取虚拟机对象
    vm = None
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for obj in container.view:
        if obj.name == vm_name:
            vm = obj
            break
    if vm is None:
        # 记录未找到虚拟机的警告日志
        append_warning_log(f"未找到名为 {vm_name} 的虚拟机")
        return False
    # 获取虚拟机的快照列表
    snapshots = vm.snapshot.rootSnapshotList
    if not snapshots:
        # 记录未找到快照的信息日志
        append_info_log(f"未找到虚拟机 {vm_name} 的快照")
    else:
        # 列出快照并记录日志
        snapshot_list = list_snapshots(snapshots)
        return append_info_log(f"找到虚拟机 {vm_name} 的快照：{snapshot_list}")
