import re
from io import StringIO
from pathlib import Path
from sh import Command, ErrorReturnCode, TimeoutException
from firepy.instance import Instance
from firepy.exceptions import FirecrackerError, err_from_returncode


REGEX_STDERR_MESSAGE = re.compile('.*? \\[[\\w -:]+\\] (.*)', re.MULTILINE)
DEFAULT_FIRECRACKER = Command('./firecracker')


class Firecracker:
    vms: list[Instance] = []
    run: Command
    _id: int = 0

    def __init__(self, command: Command = None):
        self.run = command or DEFAULT_FIRECRACKER

    def _next_free_id(self) -> int:
        # TODO: reuse ids
        next_id = self._id
        self._id += 1
        return next_id

    def _init_socket(self, socket_path: str) -> str:
        Path(socket_path).unlink(missing_ok=True)

    def _check_socket(self, socket_path: str) -> str:
        if not Path(socket_path).exists():
            raise FirecrackerError('Failed to start VM or socket missing')

    def _create_instance(self, socket_path: str = None, sleep=2) -> Instance:
        stderr = StringIO()
        try:
            self.run("--api-sock", socket_path,
                     _bg=True, _err=stderr).wait(sleep)
        except TimeoutException:
            pass
        vm = Instance(socket_path, stderr)
        self.vms.append(vm)
        return vm

    def create_vm(self, jailed=True, socket_path: str = None) -> Instance:
        vm_id = self._next_free_id()
        vm_socket_path = socket_path or f'/tmp/firecracker-{vm_id}.socket'

        try:
            self._init_socket(vm_socket_path)
            vm_instance = self._create_instance(vm_socket_path, vm_id)
            self._check_socket(vm_socket_path)
        except ErrorReturnCode as err:
            raise err_from_returncode(err) from err

        return vm_instance
