from libprobe.probe import Probe
from lib.check.proxmoxvm import check_proxmoxvm
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = {
        'proxmoxvm': check_proxmoxvm
    }

    probe = Probe("proxmoxvm", version, checks)

    probe.start()
