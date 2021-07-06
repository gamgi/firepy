from io import StringIO
from requests.exceptions import ConnectionError, HTTPError
from firepy.connection import Connection
from firepy.exceptions import err_from_stderr


class Instance:
    conn: Connection

    def __init__(self, socket_path: str, stderr: StringIO = None):
        self.conn = Connection(socket_path)
        self.stderr = stderr

    def start(self):
        try:
            self.conn.put('/actions', json={'action_type': 'InstanceStart'})
        except (ConnectionError, HTTPError) as err:
            if self.stderr is not None:
                raise err_from_stderr(self.stderr) from err
            else:
                raise

    def pause(self):
        pass

    def set_config(self, **kwargs):
        self.conn.put('/actions', json={
            **kwargs
        })

    def set_kernel(self, kernel_path: str, **kwargs):
        self.conn.put('/boot-source', json={
            "kernel_image_path": kernel_path,
            "boot_args": "console=ttyS0 reboot=k panic=1 pci=off",
            **kwargs
        })

    def set_rootfs(self, rootfs_path: str, **kwargs):
        self.conn.put('/drives/rootfs', json={
            "drive_id": "rootfs",
            "path_on_host": rootfs_path,
            "is_root_device": True,
            "is_read_only": False,
            **kwargs
        })
