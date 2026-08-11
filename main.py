from libprobe.probe import Probe
from lib.check.firewall import CheckFirewall
from lib.check.vm import CheckVm
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = (
        CheckFirewall,
        CheckVm,
    )

    probe = Probe("proxmoxvm", version, checks)
    probe.start()
