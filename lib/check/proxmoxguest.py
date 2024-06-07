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
    url = f'https://{address}:{port}/api2/json/nodes/{node}/qemu/{vmid}/'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, ssl=ssl) as resp:
            resp.raise_for_status()
            data = await resp.json()

    guest = data  # TODO
    return {
        'guest': [guest]
    }
