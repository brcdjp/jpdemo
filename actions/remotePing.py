from st2actions.runners.pythonrunner import Action
from clicrud.device.generic import generic

class remotePing(Action):
    def run(self, host, user, password, target, vrf):
        transport = generic(host=host, username=user, password=password, enable=password, method='ssh')
        cmd = 'ping {} vrf {} count 1 timeout 1'.format(target, vrf)
        result = transport.read(cmd, return_type='string')
        print result
        ok = result.find('100% packet loss') < 0
        return (ok, {'src':host, 'dst':target, 'ok':ok})
