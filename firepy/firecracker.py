from firepy.instance import Instance
from uuid import uuid4
from sh import Command


class Firecracker:
    vms: list[Instance] = []
    run: Command

    def __init__(self, run_command: Command = Command('./firecracker')):
        self.run = run_command

    def _create_socket(self) -> str:
        socket_path = f'/tmp/firecracker-{uuid4()}.socket'
        return socket_path

    def _create_instance(self, socket_path) -> Instance:
        args = {'api-sock': socket_path}
        self.run(_bg_exc=True, **args)
        vm = Instance(socket_path)
        self.vms.append(vm)
        return vm

    def create_vm(self, jailed=True) -> Instance:
        socket_path = self._create_socket()
        return self._create_instance(socket_path)
