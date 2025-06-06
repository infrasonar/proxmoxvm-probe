from libprobe.asset import Asset
from ..utils import to_percent_used
from ..helpers import api_request


async def check_vm(
        asset: Asset,
        asset_config: dict,
        config: dict) -> dict:

    uri = '/status/current'
    data = await api_request(asset, asset_config, config, uri, 'qemu')
    vm = data['data']
    balloon = vm.get('ballooninfo')
    blockstat = vm.get('blockstat')
    ha = vm.get('ha')
    nics = vm.get('nics')
    support = vm.get('proxmox-support')
    item = {
        'name': vm.get('name'),  # str
        'vmid': vm['vmid'],  # int
        'agent': bool(vm.get('agent')),  # bool
        'balloon': vm.get('balloon'),  # int/optional
        'cpu': vm.get('cpu', 0) * 100.0,  # float
        'cpus': vm.get('cpus'),  # int
        'disk': vm.get('disk'),  # int
        'diskread': vm.get('diskread'),  # int
        'diskwrite': vm.get('diskwrite'),  # int
        'freemem': vm.get('freemem'),  # int/optional
        'maxdisk': vm.get('maxdisk'),  # int
        'maxmem': vm.get('maxmem'),  # int
        'mem': vm.get('mem'),  # int
        'netin': vm.get('netin'),  # int
        'netout': vm.get('netout'),  # int
        'pid': vm.get('pid'),  # int/optional
        'qmpstatus': vm.get('qmpstatus'),  # str
        'running_machine': vm.get('running-machine'),  # str/optional
        'running_qemu': vm.get('running-qemu'),  # str/optional
        'status': vm['status'],  # str (enum: stopped | running)
        'uptime': vm.get('uptime'),  # int
    }
    state = {
        'vm': [item],
    }
    if balloon is not None:
        state['ballooninfo'] = [{
            'name': 'ballooninfo',
            'free_mem': balloon.get('free_mem'),  # int
            'major_page_faults': balloon.get('major_page_faults'),  # int
            'last_update': balloon.get('last_update'),  # int
            'minor_page_faults': balloon.get('minor_page_faults'),  # int
            'mem_swapped_out': balloon.get('mem_swapped_out'),  # int
            'actual': balloon.get('actual'),  # int
            'max_mem': balloon.get('max_mem'),  # int
            'total_mem': balloon.get('total_mem'),  # int
            'mem_swapped_in': balloon.get('mem_swapped_in'),  # int
            'percent_used':
            to_percent_used(balloon.get('total_mem'), balloon.get('free_mem')),
            'percent_used_actual':
            to_percent_used(balloon.get('actual'), balloon.get('free_mem'))
        }]
    if blockstat is not None:
        state['blockstat'] = [{
            'name': name,  # str
            'account_failed': n.get('account_failed'),  # bool
            'account_invalid': n.get('account_invalid'),  # bool
            'failed_flush_operations': n.get('failed_flush_operations'),  # int
            'failed_rd_operations': n.get('failed_rd_operations'),  # int
            'failed_unmap_operations': n.get('failed_unmap_operations'),  # int
            'failed_wr_operations': n.get('failed_wr_operations'),  # int
            'failed_zone_append_operations':
            n.get('failed_zone_append_operations'),  # int
            'flush_operations': n.get('flush_operations'),  # int
            'flush_total_time_ns': n.get('flush_total_time_ns'),  # int
            'idle_time_ns': n.get('idle_time_ns'),  # int
            'invalid_flush_operations':
            n.get('invalid_flush_operations'),  # int
            'invalid_rd_operations': n.get('invalid_rd_operations'),  # int
            'invalid_unmap_operations':
            n.get('invalid_unmap_operations'),  # int
            'invalid_wr_operations': n.get('invalid_wr_operations'),  # int
            'invalid_zone_append_operations':
            n.get('invalid_zone_append_operations'),  # int
            'rd_bytes': n.get('rd_bytes'),  # int
            'rd_merged': n.get('rd_merged'),  # int
            'rd_operations': n.get('rd_operations'),  # int
            'rd_total_time_ns': n.get('rd_total_time_ns'),  # int
            'timed_stats': n.get('rd_total_time_ns'),  # listint
            'unmap_bytes': n.get('unmap_bytes'),  # int
            'unmap_merged': n.get('unmap_merged'),  # int
            'unmap_operations': n.get('unmap_operations'),  # int
            'unmap_total_time_ns': n.get('unmap_total_time_ns'),  # int
            'wr_bytes': n.get('wr_bytes'),  # int
            'wr_highest_offset': n.get('wr_highest_offset'),  # int
            'wr_merged': n.get('wr_merged'),  # int
            'wr_operations': n.get('wr_operations'),  # int
            'wr_total_time_ns': n.get('wr_total_time_ns'),  # int
            'zone_append_bytes': n.get('zone_append_bytes'),  # int
            'zone_append_merged': n.get('zone_append_merged'),  # int
            'zone_append_operations': n.get('zone_append_operations'),  # int
            'zone_append_total_time_ns':
            n.get('zone_append_total_time_ns'),  # int
        } for name, n in blockstat.items()]
    if ha is not None:
        state['ha'] = [{
            'name': 'ha',
            'managed': bool(ha.get('managed')),  # bool
        }]
    if support is not None:
        state['proxmox_support'] = [{
            'name': 'proxmox_support',
            'backup_fleecing': support.get('backup-fleecing'),  # bool
            'backup_max_workers': support.get('backup-max-workers'),  # bool
            'pbs_dirty_bitmap': support.get('pbs-dirty-bitmap'),  # bool
            'pbs_dirty_bitmap_migration':
            support.get('pbs-dirty-bitmap-migration'),  # bool
            'pbs_dirty_bitmap_savevm':
            support.get('pbs-dirty-bitmap-savevm'),  # bool
            'pbs_library_version': support.get('pbs-library-version'),  # str
            'pbs_masterkey': support.get('pbs-masterkey'),  # bool
            'query_bitmap_info': support.get('query-bitmap-info'),  # bool
        }]
    if nics is not None:
        state['nics'] = [{
            'name': name,  # str
            'netin': n['netin'],  # int
            'netout': n['netout'],  # int
        } for name, n in nics.items()]

    return state
