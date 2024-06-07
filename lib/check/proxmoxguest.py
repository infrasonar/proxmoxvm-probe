import aiohttp
from libprobe.asset import Asset
from libprobe.exceptions import CheckException


DEFAULT_PORT = 8006


async def check_proxmoxguest(
        asset: Asset,
        asset_config: dict,
        config: dict) -> dict:
    address = config.get('address')
    if not address:
        address = asset.name
    port = config.get('port', DEFAULT_PORT)
    ssl = config.get('ssl', False)
    node = config.get('node')
    if node is None:
        raise CheckException('invalid config: missing `node`')
    vmid = config.get('vmid')
    if vmid is None:
        raise CheckException('invalid config: missing `vmid`')

    username = asset_config.get('username')
    realm = asset_config.get('realm')
    token_id = asset_config.get('token_id')
    token = asset_config.get('secret')
    if None in (username, realm, token_id, token):
        raise CheckException('missing credentials')

    headers = {
        'Authorization': f'PVEAPIToken={username}@{realm}!{token_id}={token}'
    }
    base_url = f'https://{address}:{port}'
    url = f'{base_url}/api2/json/nodes/{node}/qemu/{vmid}/status/current'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, ssl=ssl) as resp:
            resp.raise_for_status()
            data = await resp.json()

    vm = data['data']
    nics = vm.get('nics')
    item = {
        'name': str(vm['vmid']),
        # 'ha': vm['ha'],  # TODO how to interpret {managed: 0}?
        'vmid': vm['vmid'],
        'balloon': vm.get('balloon'),
        # 'ballooninfo': vm.get('ballooninfo'),  # TODO many metrics
        # 'blockstat': vm.get('blockstat'),  # TODO many metrics
        'cpu': vm.get('cpu'),
        'cpus': vm.get('cpus'),
        'disk': vm.get('disk'),
        'diskread': vm.get('diskread'),
        'diskwrite': vm.get('diskwrite'),
        'freemem': vm.get('freemem'),
        'maxdisk': vm.get('maxdisk'),
        'maxmem': vm.get('maxmem'),
        'mem': vm.get('mem'),
        'netin': vm.get('netin'),
        'netout': vm.get('netout'),
        'pid': vm.get('pid'),
        # 'proxmox-support': vm.get('proxmox-support'),  # TODO relevant?
        'qmpstatus': vm.get('qmpstatus'),
        'running_machine': vm.get('running-machine'),
        'running_qemu': vm.get('running-qemu'),
        'status': vm['status'],
        'uptime': vm.get('uptime'),
        'vm_name': vm.get('name'),
    }
    state = {
        'guest': [item],
    }
    if nics is not None:
        state['nics'] = [{
            'name': name,
            'netin': n['netin'],
            'netout': n['netout'],
        } for name, n in nics.items()]

    return state
