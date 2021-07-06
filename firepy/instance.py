from functools import wraps
from io import StringIO
from requests.exceptions import ConnectionError, HTTPError
from firepy.connection import Connection
from firepy.exceptions import err_from_stderr, FirecrackerApiError


def handle_errors(func):
    """Decorator that humanizes exceptions.

    It
    - parses firecracker HTTP responses
    - checks instance stderr for error messages
    """
    @wraps(func)
    def wrapper(self: 'Instance', *args, **kwargs):
        try:
            func(self, *args, **kwargs)
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
    return wrapper


class Instance:
    conn: Connection

    def __init__(self, socket_path: str, stderr: StringIO = None):
        self.conn = Connection(socket_path)
        self.stderr = stderr
        # TODO check socket exists

    @handle_errors
    def start(self):
        self.conn.put('/actions', json={'action_type': 'InstanceStart'})

    @handle_errors
    def pause(self):
        self.conn.put('/vm', json={'state': 'Paused'})

    @handle_errors
    def resume(self):
        self.conn.put('/vm', json={'state': 'Resumed'})

    @handle_errors
    def set_config(self, **kwargs):
        self.conn.put('/machine-config', json={
            **kwargs
        })

    @handle_errors
    def set_kernel(self, kernel_path: str, **kwargs):
        self.conn.put('/boot-source', json={
            "kernel_image_path": kernel_path,
            "boot_args": "console=ttyS0 reboot=k panic=1 pci=off",
            **kwargs
        })

    @handle_errors
    def set_rootfs(self, rootfs_path: str, **kwargs):
        self.conn.put('/drives/rootfs', json={
            "drive_id": "rootfs",
            "path_on_host": rootfs_path,
            "is_root_device": True,
            "is_read_only": False,
            **kwargs
        })

    @handle_errors
    def create_snapshot(self, snapshot_path: str, mem_file_path: str,
                        snapshot_type='Full', **kwargs):
        self.conn.put('/snapshot/create', json={
            "snapshot_type": snapshot_type,
            "snapshot_path": snapshot_path,
            "mem_file_path": mem_file_path,
            **kwargs
        })

    @handle_errors
    def load_snapshot(self, snapshot_path: str, mem_file_path: str,
                      resume_vm=True, **kwargs):
        self.conn.put('/snapshot/load', json={
            "snapshot_path": snapshot_path,
            "mem_file_path": mem_file_path,
            "resume_vm": resume_vm,
            **kwargs
        })
