import re
from pathlib import Path
from uuid import uuid4
from sh import Command, ErrorReturnCode, TimeoutException
from firepy.instance import Instance
from firepy.exceptions import err_from_stderr


REGEX_STDERR_MESSAGE = re.compile('.*? \\[[\\w -:]+\\] (.*)', re.MULTILINE)


class Firecracker:
    vms: list[Instance] = []
    run: Command

    def __init__(self, run_command: Command = Command('./firecracker')):
        self.run = run_command

    def _create_socket(self, override: str = None) -> str:
        socket_path = override or f'/tmp/firecracker-{uuid4()}.socket'
        Path(socket_path).unlink(missing_ok=True)
        return socket_path

    def _create_instance(self, socket_path, sleep=2) -> Instance:
        try:
            self.run("--api-sock", socket_path, _bg=True,
                     _bg_exc=True).wait(sleep)
        except TimeoutException:
            pass
        vm = Instance(socket_path)
        self.vms.append(vm)
        return vm

    def create_vm(self, jailed=True, socket_path: str = None) -> Instance:
        _socket_path = self._create_socket(socket_path)
        try:
            return self._create_instance(_socket_path)
        except ErrorReturnCode as err:
            raise err_from_stderr(err) from err
