from st2actions.runners.pythonrunner import Action
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import atexit

class ShutVnicSelect(Action):
    def run(self, host, user, password, port, vmname, vnics):
        session = SmartConnect(host=host, user=user, pwd=password, port=port)
        atexit.register(Disconnect, session)
        content = session.RetrieveContent()
        vms = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True).view
        found = filter(lambda x: x.name == vmname, vms)
        if not found:
            return (False, "VM {0} not found\n".format(vmname))
        result = []
        for nic in filter(lambda d: d.deviceInfo.label in vnics, found[0].config.hardware.device):
            devspec = vim.vm.device.VirtualDeviceSpec()
            devspec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
            devspec.device = nic
            conn = vim.vm.device.VirtualDevice.ConnectInfo()
            conn.connected = False
            conn.startConnected = False
            devspec.device.connectable = conn
            spec = vim.vm.ConfigSpec()
            spec.deviceChange = [devspec]
            task = found[0].ReconfigVM_Task(spec=spec)
            print '{0:<19} {1:<18} Down'.format(nic.deviceInfo.label, nic.macAddress)
            result.append((nic.deviceInfo.label, nic.macAddress))
        return (True, result)
