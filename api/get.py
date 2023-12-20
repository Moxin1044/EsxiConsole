import ssl
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import requests, os
import urllib3
from requests.auth import HTTPBasicAuth
from modules import get_configs, append_info_log, append_error_log, append_warning_log

# Disable SSL certificate verification
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Replace with your ESXi host's IP address, username, and password
esxi_host = get_configs()['EsxiAddr']
esxi_user = get_configs()['EsxiUser']
esxi_password = get_configs()['EsxiPass']

# Check if ESXi host is reachable
def check_esxi_host():
    si = SmartConnect(host=esxi_host, user=esxi_user, pwd=esxi_password, port=443, sslContext=ssl_context)
    content = si.RetrieveContent()
    Disconnect(si)
    if content:
        return True
    return False

# Get information about all virtual machines on the ESXi host
def get_all_esxi_machines():
    si = SmartConnect(host=esxi_host, user=esxi_user, pwd=esxi_password, port=443, sslContext=ssl_context)
    content = si.RetrieveContent()
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    vms = vm_view.view
    data = {}
    i = 0
    for vm in vms:
        # Get disk size
        virtual_disks = [device for device in vm.config.hardware.device if isinstance(device, vim.vm.device.VirtualDisk)]
        disk_capacity_bytes = sum(disk.capacityInBytes for disk in virtual_disks)
        # Collect virtual machine information
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
    Disconnect(si)
    append_info_log(f"ESXi Virtual Machine List: {data}")
    return data

# Get screenshot of a specific virtual machine on the ESXi host
def get_esxi_machines_screenshot(vm_name):
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
        urllib3.disable_warnings()
        screenshot_url = f'https://{esxi_host}:443/screen?id={target_vm._moId}'
        append_info_log(f"Getting screenshot for ID: {target_vm._moId} ({vm_name})")
        auth = HTTPBasicAuth(esxi_user, esxi_password)
        response = requests.get(screenshot_url, verify=False, auth=auth)
        Disconnect(si)
        if response.status_code == 200:
            add = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'log', 'screenhost', f'{target_vm._moId}screenshot.png')
            with open(add, 'wb') as file:
                file.write(response.content)
            append_info_log(f"Successfully obtained screenshot for ID: {target_vm._moId} ({vm_name}): {add}")
            return add
        else:
            append_error_log(f"Unable to get screenshot for ID: {target_vm._moId} ({vm_name}): Connection may be unavailable. Status code: {response.status_code}")
            return False
    else:
        append_warning_log(f"Unable to get screenshot for {vm_name}: Virtual machine not found or does not exist.")
        return False

# Recursive function for listing snapshots
def list_snapshots(snapshot_tree, snap_list=None):
    if snap_list is None:
        snap_list = []
    for snapshot in snapshot_tree:
        snap_list.append({
            "name": snapshot.name,
            "description": snapshot.description,
            "createTime": f"{snapshot.createTime}"
        })
        if snapshot.childSnapshotList:
            list_snapshots(snapshot.childSnapshotList, snap_list)
    return snap_list

# List snapshots for a specific virtual machine on the ESXi host
def get_esxi_machines_snapshots(vm_name):
    si = SmartConnect(host=esxi_host, user=esxi_user, pwd=esxi_password, port=443, sslContext=ssl_context)
    content = si.RetrieveContent()
    vm = None
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for obj in container.view:
        if obj.name == vm_name:
            vm = obj
            break
    if vm is None:
        append_warning_log(f"Virtual machine with the name {vm_name} not found")
        return False
    snapshots = vm.snapshot.rootSnapshotList
    if not snapshots:
        append_info_log(f"No snapshots found for virtual machine {vm_name}")
    else:
        snapshot_list = list_snapshots(snapshots)
        return append_info_log(f"Snapshots found for virtual machine {vm_name}: {snapshot_list}")
