from libprobe.probe import Probe
from lib.check.vm import check_vm
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = {
        'vm': check_vm
    }

    probe = Probe("proxmoxvm", version, checks)

    probe.start()
