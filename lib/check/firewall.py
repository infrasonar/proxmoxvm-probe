from libprobe.asset import Asset
from libprobe.check import Check
from ..utils import to_percent_used
from ..helpers import api_request


class CheckFirewall(Check):
    key = 'firewall'
    unchanged_eol = 14400

    @staticmethod
    async def run(asset: Asset, local_config: dict, config: dict) -> dict:
        uri = '/firewall/options'
        data = await api_request(asset, local_config, config, uri, 'qemu')
        firewall = data['data']
        item = {
            'name': 'firewall',
            'dhcp': firewall.get('dhcp', False),  # bool
            'enable': firewall.get('enable', False),  # bool
            'ipfilter': firewall.get('ipfilter'),  # bool/optional
            'log_level_in': firewall.get('log_level_in'),  # str/optional
            'log_level_out': firewall.get('log_level_out'),  # str/optional
            'macfilter': firewall.get('macfilter', True),  # bool
            'ndp': firewall.get('ndp', True),  # bool
            'policy_in': firewall.get('policy_in'),  # str/optional
            'policy_out': firewall.get('policy_out'),  # str/optional
            'radv': firewall.get('radv'),  # bool/optional
            'digest': firewall.get('digest'),  # str/optional
        }
        state = {
            'firewall': [item],
        }

        return state