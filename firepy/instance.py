from firepy.connection import Connection


class Instance:
    conn: Connection

    def __init__(self, socket_path: str):
        self.conn = Connection(socket_path)

    def start(self):
        self.conn.put(json={'action_type': 'InstanceStart'})

    def pause(self):
        pass

    def set_kernel(self, kernel_path: str, **kwargs):
        self.conn.put(json={
            "kernel_image_path": kernel_path,
            "boot_args": "console=ttyS0 reboot=k panic=1 pci=off",
            **kwargs
        })

    def set_rootfs(self, rootfs_path: str, **kwargs):
        self.conn.put(json={
            "drive_id": "rootfs",
            "path_on_host": rootfs_path,
            "is_root_device": True,
            "is_read_only": False,
            **kwargs
        })
