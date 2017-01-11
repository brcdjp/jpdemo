from st2actions.runners.pythonrunner import Action
from netmiko import ConnectHandler

class CliAction(Action):
    def run(self,host, cmd):
        net_connect = ConnectHandler(device_type='brocade_vdx',ip=host,username='admin',password='password')
        output = net_connect.send_command(cmd)
        print output
        return (True, output)

