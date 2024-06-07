from libprobe.probe import Probe
from lib.check.proxmoxguest import check_proxmoxguest
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = {
        'proxmoxguest': check_proxmoxguest
    }

    probe = Probe("proxmoxguest", version, checks)

    probe.start()
