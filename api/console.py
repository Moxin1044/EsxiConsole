import ssl
import time

from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim

from modules import get_configs, append_info_log, append_error_log, append_warning_log

# 禁用 SSL 证书验证
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# 替换为你的 ESXi 主机的 IP 地址、用户名和密码
esxi_host = get_configs()['EsxiAddr']
esxi_user = get_configs()['EsxiUser']
esxi_password = get_configs()['EsxiPass']


# 重启虚拟机
def reboot_esxi_machines(vm_name):
    # 连接到 ESXi 主机
    si = SmartConnect(host=esxi_host, user=esxi_user, pwd=esxi_password, port=443, sslContext=ssl_context)

    # 获取虚拟机列表
    content = si.RetrieveContent()
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    vms = vm_view.view

    # 查找要重启的虚拟机
    target_vm = None
    for vm in vms:
        if vm.name == vm_name:
            target_vm = vm
            break

    # 重启虚拟机
    if target_vm:
        try:
            target_vm.RebootGuest()
            append_info_log(f"虚拟机 {vm_name} 已重启")
        except vim.fault.ToolsUnavailable:
            append_error_log(f"虚拟机 {vm_name} 中的 VMware Tools 不可用，无法执行重启操作")
    else:
        append_warning_log(f"无法重启 {vm_name} 虚拟机：无法找到/不存在该虚拟机。")

    # 断开连接
    Disconnect(si)


# 关闭虚拟机电源
def poweroff_esxi_machines(vm_name):
    # 连接到 ESXi 主机
    si = SmartConnect(host=esxi_host, user=esxi_user, pwd=esxi_password, port=443, sslContext=ssl_context)

    # 获取虚拟机列表
    content = si.RetrieveContent()
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    vms = vm_view.view

    # 查找要重启的虚拟机
    target_vm = None
    for vm in vms:
        if vm.name == vm_name:
            target_vm = vm
            break

    # 关闭虚拟机
    if target_vm:
        try:
            target_vm.PowerOff()
            append_info_log(f"虚拟机 {vm_name} 已关闭")
        except vim.fault.ToolsUnavailable:
            append_error_log(f"虚拟机 {vm_name} 中的 VMware Tools 不可用，无法执行关闭操作")
    else:
        append_warning_log(f"无法关闭 {vm_name} 虚拟机：无法找到/不存在该虚拟机。")

    # 断开连接
    Disconnect(si)


# 关机操作
def shutdown_esxi_machines(vm_name):
    # 连接到 ESXi 主机
    si = SmartConnect(host=esxi_host, user=esxi_user, pwd=esxi_password, port=443, sslContext=ssl_context)

    # 获取虚拟机列表
    content = si.RetrieveContent()
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    vms = vm_view.view

    # 查找要重启的虚拟机
    target_vm = None
    for vm in vms:
        if vm.name == vm_name:
            target_vm = vm
            break

    # 关机虚拟机
    if target_vm:
        try:
            target_vm.ShutdownGuest()
            append_info_log(f"虚拟机 {vm_name} 已关机")
        except vim.fault.ToolsUnavailable:
            append_error_log(f"虚拟机 {vm_name} 中的 VMware Tools 不可用，无法执行关机操作")
    else:
        append_warning_log(f"无法关机 {vm_name} 虚拟机：无法找到/不存在该虚拟机。")

    # 断开连接
    Disconnect(si)


# 开启虚拟机电源
def poweron_esxi_machines(vm_name):
    # 连接到 ESXi 主机
    si = SmartConnect(host=esxi_host, user=esxi_user, pwd=esxi_password, port=443, sslContext=ssl_context)

    # 获取虚拟机列表
    content = si.RetrieveContent()
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    vms = vm_view.view

    # 查找要重启的虚拟机
    target_vm = None
    for vm in vms:
        if vm.name == vm_name:
            target_vm = vm
            break

    # 开启虚拟机
    if target_vm:
        try:
            target_vm.PowerOn()
            append_info_log(f"虚拟机 {vm_name} 已开机")
        except vim.fault.ToolsUnavailable:
            append_error_log(f"虚拟机 {vm_name} 中的 VMware Tools 不可用，无法执行开机操作")
    else:
        append_warning_log(f"无法开机 {vm_name} 虚拟机：无法找到/不存在该虚拟机。")

    # 断开连接
    Disconnect(si)


# 重置虚拟机
def reset_esxi_machines(vm_name):
    # 连接到 ESXi 主机
    si = SmartConnect(host=esxi_host, user=esxi_user, pwd=esxi_password, port=443, sslContext=ssl_context)

    # 获取虚拟机列表
    content = si.RetrieveContent()
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    vms = vm_view.view

    # 查找要重启的虚拟机
    target_vm = None
    for vm in vms:
        if vm.name == vm_name:
            target_vm = vm
            break

    # 重置虚拟机
    if target_vm:
        try:
            target_vm.Reset()
            append_info_log(f"虚拟机 {vm_name} 已重置")
        except vim.fault.ToolsUnavailable:
            append_error_log(f"虚拟机 {vm_name} 中的 VMware Tools 不可用，无法执行重置操作")
    else:
        append_warning_log(f"无法重置 {vm_name} 虚拟机：无法找到/不存在该虚拟机。")

    # 断开连接
    Disconnect(si)


# 挂起虚拟机
def suspend_esxi_machines(vm_name):
    # 连接到 ESXi 主机
    si = SmartConnect(host=esxi_host, user=esxi_user, pwd=esxi_password, port=443, sslContext=ssl_context)

    # 获取虚拟机列表
    content = si.RetrieveContent()
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    vms = vm_view.view

    # 查找要重启的虚拟机
    target_vm = None
    for vm in vms:
        if vm.name == vm_name:
            target_vm = vm
            break

    # 挂起虚拟机
    if target_vm:
        try:
            target_vm.Suspend()
            append_info_log(f"虚拟机 {vm_name} 已挂起")
        except vim.fault.ToolsUnavailable:
            append_error_log(f"虚拟机 {vm_name} 中的 VMware Tools 不可用，无法执行挂起操作")
    else:
        append_warning_log(f"无法挂起 {vm_name} 虚拟机：无法找到/不存在该虚拟机。")

    # 断开连接
    Disconnect(si)


# 休眠虚拟机
def standby_esxi_machines(vm_name):
    # 连接到 ESXi 主机
    si = SmartConnect(host=esxi_host, user=esxi_user, pwd=esxi_password, port=443, sslContext=ssl_context)

    # 获取虚拟机列表
    content = si.RetrieveContent()
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    vms = vm_view.view

    # 查找要重启的虚拟机
    target_vm = None
    for vm in vms:
        if vm.name == vm_name:
            target_vm = vm
            break

    # 休眠虚拟机
    if target_vm:
        try:
            target_vm.StandbyGuest()
            append_info_log(f"虚拟机 {vm_name} 已休眠")
        except vim.fault.ToolsUnavailable:
            append_error_log(f"虚拟机 {vm_name} 中的 VMware Tools 不可用，无法执行休眠操作")
    else:
        append_warning_log(f"无法休眠 {vm_name} 虚拟机：无法找到/不存在该虚拟机。")

    # 断开连接
    Disconnect(si)


# 销毁虚拟机
def destroy_esxi_machines(vm_name):
    # 连接到 ESXi 主机
    si = SmartConnect(host=esxi_host, user=esxi_user, pwd=esxi_password, port=443, sslContext=ssl_context)

    # 获取虚拟机列表
    content = si.RetrieveContent()
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    vms = vm_view.view

    # 查找要重启的虚拟机
    target_vm = None
    for vm in vms:
        if vm.name == vm_name:
            target_vm = vm
            break

    # 销毁虚拟机
    if target_vm:
        try:
            target_vm.Destroy()
            append_info_log(f"虚拟机 {vm_name} 已销毁")
        except vim.fault.ToolsUnavailable:
            append_error_log(f"虚拟机 {vm_name} 中的 VMware Tools 不可用，无法执行销毁操作")
    else:
        append_warning_log(f"无法销毁 {vm_name} 虚拟机：无法找到/不存在该虚拟机。")

    # 断开连接
    Disconnect(si)


def rename_esxi_machines(old_vm_name, new_vm_name):
    # 连接到 ESXi 主机
    si = SmartConnect(host=esxi_host, user=esxi_user, pwd=esxi_password, port=443, sslContext=ssl_context)

    # 获取虚拟机列表
    content = si.RetrieveContent()
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    vms = vm_view.view

    # 查找要重命名的虚拟机
    target_vm = None
    for vm in vms:
        if vm.name == old_vm_name:
            target_vm = vm
            break

    # 重命名虚拟机
    if target_vm:
        try:
            task = target_vm.Rename_Task(newName=new_vm_name)
            # 等待任务完成
            task_info = task.info
            while task_info.state not in [vim.TaskInfo.State.success, vim.TaskInfo.State.error]:
                task_info = task.info
            if task_info.state == vim.TaskInfo.State.success:
                append_info_log(f"虚拟机 {old_vm_name} 已成功重命名为 {new_vm_name}")
            else:
                append_error_log(f"重命名虚拟机时出现错误: {task_info.error}")
        except Exception as e:
            append_error_log(f"无法重命名虚拟机: {e}")
    else:
        append_warning_log(f"未找到名为 {old_vm_name} 的虚拟机")

    # 断开连接
    Disconnect(si)


# 拍摄快照
def create_snapshot_esxi_machine(vm_name, snapshot_name, snapshot_desc):
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

    # 创建快照
    task = vm.CreateSnapshot_Task(name=snapshot_name, description=snapshot_desc, memory=False, quiesce=False)
    while task.info.state == vim.TaskInfo.State.running:
        time.sleep(1)

    if task.info.state == vim.TaskInfo.State.success:
        append_info_log(f"虚拟机 {vm_name} 快照完成 {snapshot_name}")
        return True
    elif task.info.state == vim.TaskInfo.State.error:
        append_error_log(f"虚拟机 {vm_name} 快照 {snapshot_name} 失败: {task.info.error.msg}")
        return False


# 删除快照
def delete_snapshot(vm_name, snapshot_name):
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

    # 获取虚拟机的所有快照
    snapshots = vm.snapshot.rootSnapshotList
    if not snapshots:
        append_warning_log(f"未找到 {vm_name} 虚拟机的快照")
        return False
    else:
        # 在快照列表中查找指定的快照
        target_snapshot = None
        for snapshot in snapshots:
            if snapshot.name == snapshot_name:
                target_snapshot = snapshot
                break

        if target_snapshot is None:
            append_warning_log(f"找不到 {vm_name} 的快照 {snapshot_name}")
        else:
            # 删除指定的快照
            task = target_snapshot.snapshot.RemoveSnapshot_Task(removeChildren=False)
            while task.info.state == vim.TaskInfo.State.running:
                time.sleep(1)

            if task.info.state == vim.TaskInfo.State.success:
                append_info_log(f"已对 {vm_name} 进行删除 {snapshot_name} 快照")
                return True
            elif task.info.state == vim.TaskInfo.State.error:
                append_warning_log(f"对 {vm_name} 的快照 {snapshot_name} 删除的过程出现了 {task.info.error.msg}")
                return False


# 恢复快照
def revert_to_snapshot(vm_name, snapshot_name):
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

    # 获取虚拟机的所有快照
    snapshots = vm.snapshot.rootSnapshotList
    if not snapshots:
        append_warning_log(f"未找到 {vm_name} 虚拟机的快照")
    else:
        # 在快照列表中查找指定的快照
        target_snapshot = None
        for snapshot in snapshots:
            if snapshot.name == snapshot_name:
                target_snapshot = snapshot
                break

        if target_snapshot is None:
            append_warning_log(f"找不到 {vm_name} 的快照 {snapshot_name}")
        else:
            # 恢复到指定的快照
            task = target_snapshot.snapshot.RevertToSnapshot_Task()
            while task.info.state == vim.TaskInfo.State.running:
                time.sleep(1)

            if task.info.state == vim.TaskInfo.State.success:
                append_info_log(f"已对 {vm_name} 进行恢复 {snapshot_name} 快照")
                return True
            elif task.info.state == vim.TaskInfo.State.error:
                append_warning_log(f"对 {vm_name} 的快照 {snapshot_name} 恢复的过程出现了 {task.info.error.msg}")
                return False
