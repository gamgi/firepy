# Firepy

Firecracker bindings for Python.

## Usage

```py
from firepy import Firecracker
from pathlib import Path
kernel = Path('./vmlinux.bin')
rootfs = Path('./hello-rootfs.ext4')
fc = Firecracker('./firecracker')

vm = fc.create_vm(socket_path='/tmp/firecracker-dev.socket')
vm.set_kernel(str(kernel.absolute()))
vm.set_rootfs(str(rootfs.absolute()))
vm.create_network_interface()

vm.start()
vm.wait()
```

## Troubleshooting

> Firecracker panicked at 'Error creating the Kvm object'

Make sure the [prerequisites](https://github.com/firecracker-microvm/firecracker/blob/main/docs/getting-started.md#prerequisites) for firecracker are fulfilled.

> Could not create Network Device: TapOpen(IoctlError(Os { code: 1, kind: PermissionDenied, message: "Operation not permitted")

Host may not have permissions.


## Developing

### Getting started

```bash
make dev
pipenv install
```