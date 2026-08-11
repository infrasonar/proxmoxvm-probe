from libprobe.asset import Asset
from libprobe.check import Check
from ..helpers import api_request
from ..utils import to_bool


class CheckFirewall(Check):
    key = 'firewall'
    unchanged_eol = 14400

    @staticmethod
    async def run(asset: Asset, local_config: dict, config: dict) -> dict:
        uri = '/firewall/options'
        data = await api_request(asset, local_config, config, uri, 'qemu')
        options = data['data']
        options_item = {
            'name': 'options',
            'dhcp': to_bool(options.get('dhcp')),  # bool/optional
            'enable': to_bool(options.get('enable')),  # bool/optional
            'ipfilter': options.get('ipfilter'),  # bool/optional
            'log_level_in': options.get('log_level_in'),  # str/optional
            'log_level_out': options.get('log_level_out'),  # str/optional
            'macfilter': to_bool(options.get('macfilter')),  # bool/optional
            'ndp': to_bool(options.get('ndp')),  # bool/optional
            'policy_in': options.get('policy_in'),  # str/optional
            'policy_out': options.get('policy_out'),  # str/optional
            'radv': options.get('radv'),  # bool/optional
            'digest': options.get('digest'),  # str/optional
        }

        uri = '/firewall/rules'
        data = await api_request(asset, local_config, config, uri, 'qemu')
        rules = [
            {
                'name': str(rule['pos']),  # str
                'action': rule['action'],   # str
                'type': rule['type'],  # str
                'enable': to_bool(rule.get('enable')),  # bool/optional
                'digest': rule.get('digest'),  # str/optional
            }
            for rule in data['data']
        ]

        state = {
            'options': [options_item],
            'rules': rules,
        }

        return state
