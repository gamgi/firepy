from typing import Union
import re
from io import StringIO
from pathlib import Path
from sh import Command, ErrorReturnCode, TimeoutException
from firepy.vm import Vm
from firepy.exceptions import err_from_returncode
from firepy.tap import Tap
from firepy.utils.logging_utils import logger
from firepy.utils.network_utils import network_tap_name

REGEX_STDERR_MESSAGE = re.compile('.*? \\[[\\w -:]+\\] (.*)', re.MULTILINE)
DEFAULT_COMMAND = Command('./firecracker')


class Firecracker:
    vms: list[Vm] = []
    run: Command
    _id: int = 0

    def __init__(self, command: Union[str, Command] = DEFAULT_COMMAND):
        if isinstance(command, str):
            self.run = Command(command)
        else:
            self.run = command

    def _next_free_id(self) -> int:
        # TODO: reuse ids
        next_id = self._id
        self._id += 1
        return next_id

    def _init_socket(self, socket_path: str) -> str:
        Path(socket_path).unlink(missing_ok=True)

    # def _check_socket(self, socket_path: str) -> str:
    #     if not Path(socket_path).exists():
    #         raise FirecrackerError('Failed to start VM or socket missing')

    def _create_vm(self, id: int, socket_path: str, vm_tap_name: str, sleep=2,
                   stdout: StringIO = None, stdin: StringIO = None) -> Vm:
        Tap.create(vm_tap_name, host_ip="172.16.0.1")

        stderr = StringIO()
        handle = self.run("--api-sock", socket_path,
                          _bg=True, _err=stderr, _out=stdout, _in=stdin)

        try:
            handle.wait(sleep)
        except TimeoutException:
            pass

        vm = Vm(id, socket_path, stderr, handle)
        self.vms.append(vm)
        return vm

    def create_vm(self, jailed=True, socket_path: str = None, **kwargs) -> Vm:
        vm_id = self._next_free_id()
        vm_tap_name = network_tap_name(vm_id)
        vm_socket_path = socket_path or f'/tmp/firecracker-{vm_id}.socket'

        try:
            self._init_socket(vm_socket_path)
            vm = self._create_vm(vm_id, vm_socket_path, vm_tap_name, **kwargs)
            logger.info(f'created VM with with socket {vm_socket_path}')
            # self._check_socket(vm_socket_path)
        except ErrorReturnCode as err:
            raise err_from_returncode(err) from err

        return vm
