def network_ip(id: int) -> str:
    return f'169.254.{(4 * id + 1) // 256}.{(4 * id + 1) % 256}'


def network_mac(id: int) -> str:
    return f'02:FC:00:00:{id // 256:02x}:{id % 256:02x}'


def network_args(id: int, **kwargs):
    fc_ip = network_ip(id)
    tap_ip = fc_ip
    mask = "255.255.255.252"
    return {
        'ipv6.disable': '1',
        'ip': f'{fc_ip}::{tap_ip}:{mask}::eth0:off'
    }


def network_tap_name(id: int) -> str:
    return f'fc-{id}-tap0'
