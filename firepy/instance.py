from io import StringIO
from requests.exceptions import ConnectionError, HTTPError
from firepy.connection import Connection
from firepy.exceptions import err_from_stderr, FirecrackerApiError


class Instance:
    conn: Connection

    def __init__(self, socket_path: str, stderr: StringIO = None):
        self.conn = Connection(socket_path)
        self.stderr = stderr

    def _put(self, path: str, **kwargs):
        try:
            self.conn.put(path, **kwargs)
        except HTTPError as err:
            res = err.response.json()
            if 'fault_message' in res:
                raise FirecrackerApiError(res['fault_message'])
            raise
        except ConnectionError as err:
            if self.stderr is not None:
                raise err_from_stderr(self.stderr) from err
            else:
                raise

    def start(self):
        self._put('/actions', json={'action_type': 'InstanceStart'})

    def pause(self):
        pass

    def set_config(self, **kwargs):
        self._put('/machine-config', json={
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
