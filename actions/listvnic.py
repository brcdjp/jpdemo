from st2actions.runners.pythonrunner import Action
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import atexit

class ListVnic(Action):
    def run(self, host, user, password, port, vmname):
        session = SmartConnect(host=host, user=user, pwd=password, port=port)
        atexit.register(Disconnect, session)
        content = session.RetrieveContent()
        vms = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True).view
        found = filter(lambda x: x.name == vmname, vms)
        if not found:
            return (False, "VM {0} not found\n".format(vmname))
        result = []
        for nic in filter(lambda d: isinstance(d, vim.vm.device.VirtualEthernetCard), found[0].config.hardware.device):
            print '{0:<19} {1:<18}'.format(nic.deviceInfo.label, nic.macAddress)
            result.append(nic.deviceInfo.label)
        return (True, result)
