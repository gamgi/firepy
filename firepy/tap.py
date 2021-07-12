from sh import ip, iptables, sysctl, ErrorReturnCode


class Tap:
    @staticmethod
    def create(tap_name: str, host_ip: str):
        try:
            # create tap device
            ip("tuntap", "add", tap_name, "mode", "tap")

            # configure firewall
            ip("addr", "add", host_ip + "/24", "dev", tap_name)
            ip("link", "set", tap_name, "up")
            # TODO: use /etc/sysctl.conf instead
            sysctl("-w", "net.ipv4.ip_forward=1")
            iptables("-t", "nat", "-A", "POSTROUTING",
                     "-o", "eth0", "-j", "MASQUERADE")
            iptables("-A", "FORWARD", "-m", "conntrack", "--ctstate",
                     "RELATED,ESTABLISHED", "-j" "ACCEPT")
            iptables("-A", "FORWARD", "-i", tap_name,
                     "-o", "eth0", "-j", "ACCEPT")
        except ErrorReturnCode as err:
            raise RuntimeError(
                f'failed to create tap device "{tap_name}": {err}') from err

    def remove(tap_name: str):
        ip("link", "del", tap_name)
