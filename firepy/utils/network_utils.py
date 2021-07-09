def network_ip(id: int) -> str:
    return f'172.16.{(4 * id + 2) // 256}.{(4 * id + 2) % 256}'


def network_mac(id: int) -> str:
    return f'02:FC:00:00:{id // 256:02x}:{id % 256:02x}'


def network_tap_name(id: int) -> str:
    return f'fc-{id}-tap0'
