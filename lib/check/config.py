from libprobe.asset import Asset
from libprobe.check import Check
from ..helpers import api_request
from ..utils import to_bool, to_int


class CheckConfig(Check):
    key = 'config'
    unchanged_eol = 14400

    @staticmethod
    async def run(asset: Asset, local_config: dict, config: dict) -> dict:
        uri = '/config'
        data = await api_request(asset, local_config, config, uri, 'qemu')
        config = data['data']
        config_item = {
            'name': config.get('name'),  # str
            'boot': config.get('boot'),  # str
            'cpu': config.get('cpu'),  # str
            'digest': config.get('digest'),  # str
            'memory': to_int(config.get('memory')),  # int
            'meta': config.get('meta'),  # str
            'net0': config.get('net0'),  # str
            'numa': to_bool(config.get('numa')),  # bool
            'onboot': to_bool(config.get('onboot')),  # bool
            'ostype': config.get('ostype'),  # str
            'scsi0': config.get('scsi0'),  # str
            'scsihw': config.get('scsihw'),  # str
            'smbios1': config.get('smbios1'),  # str
            'sockets': config.get('sockets'),  # int
            'vmgenid': config.get('vmgenid'),  # str
        }

        state = {
            'config': [config_item],
        }

        return state
