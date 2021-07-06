from firepy.instance import Instance


class TestInstance:
    def test_start_vm(self, requests_mock):
        m = requests_mock.put('http+unix://%2Ftmp%2Ftest.socket/actions')
        vm = Instance('/tmp/test.socket')
        vm.start()

        assert m.last_request.json() == {'action_type': 'InstanceStart'}

    def test_set_kernel(self, requests_mock):
        m = requests_mock.put('http+unix://%2Ftmp%2Ftest.socket/boot-source')
        vm = Instance('/tmp/test.socket')
        vm.set_kernel('/tmp/example.ext4')

        assert m.last_request.json() == {
            "kernel_image_path": '/tmp/example.ext4',
            "boot_args": "console=ttyS0 reboot=k panic=1 pci=off",
        }

    def test_set_rootfs(self, requests_mock):
        m = requests_mock.put('http+unix://%2Ftmp%2Ftest.socket/drives/rootfs')
        vm = Instance('/tmp/test.socket')
        vm.set_rootfs('/tmp/example.ext4')

        assert m.last_request.json() == {
            'drive_id': 'rootfs',
            'is_read_only': False,
            'is_root_device': True,
            'path_on_host': '/tmp/example.ext4',
        }
