def network_ip(id: int) -> str:
    return f'169.254.{(4 * id + 1) // 256}.{(4 * id + 1) % 256}'


def network_mac(id: int) -> str:
    return f'02:FC:00:00:{id // 256:02x}:{id % 256:02x}'


def network_tap_name(id: int) -> str:
    return 'tap0'
    # return f'fc-{id}-tap0'
