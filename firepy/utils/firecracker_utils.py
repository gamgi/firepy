from firepy.utils.network_utils import network_ip


def boot_args_str(args: dict):
    return ' '.join([f'{k}={v}' for k, v in args.items()])


def kernel_network_boot_args(id: int) -> dict:
    fc_ip = network_ip(id)
    tap_ip = fc_ip
    mask = "255.255.255.255"
    return {
        'ipv6.disable': '1',
        'ip': f'{fc_ip}::{tap_ip}:{mask}::eth0:off'
    }


def kernel_boot_args(id: int, override_boot_args: dict = {}) -> str:
    return boot_args_str({
        'console': 'ttyS0',
        'reboot': 'k',
        'panic': '1',
        'pci': 'off',
        **kernel_network_boot_args(id),
        **override_boot_args,
    })
