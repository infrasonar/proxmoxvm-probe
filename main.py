from libprobe.probe import Probe
from lib.check.xxx import check_xxx
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = {
        'xxx': check_xxx
    }

    probe = Probe("proxmoxguest", version, checks)

    probe.start()
