from firepy.vm import Vm


class TestVm:
    def test_start_vm(self, requests_mock):
        m = requests_mock.put('http+unix://%2Ftmp%2Ftest.socket/actions')
        vm = Vm(0, '/tmp/test.socket')
        vm.start()

        assert m.last_request.json() == {'action_type': 'InstanceStart'}

    def test_pause_vm(self, requests_mock):
        m = requests_mock.put('http+unix://%2Ftmp%2Ftest.socket/vm')
        vm = Vm(0, '/tmp/test.socket')
        vm.pause()

        assert m.last_request.json() == {
            "state": 'Paused',
        }

    def test_set_kernel(self, requests_mock):
        m = requests_mock.put('http+unix://%2Ftmp%2Ftest.socket/boot-source')
        vm = Vm(0, '/tmp/test.socket')
        vm.set_kernel('/tmp/example.ext4')

        assert m.last_request.json() == {
            "kernel_image_path": '/tmp/example.ext4',
            "boot_args": "console=ttyS0 reboot=k panic=1 pci=off " +
            "ipv6.disable=1 " +
            "ip=172.16.0.2::172.16.0.2:255.255.255.255::eth0:off",
        }

    def test_set_rootfs(self, requests_mock):
        m = requests_mock.put('http+unix://%2Ftmp%2Ftest.socket/drives/rootfs')
        vm = Vm(0, '/tmp/test.socket')
        vm.set_rootfs('/tmp/example.ext4')

        assert m.last_request.json() == {
            'drive_id': 'rootfs',
            'is_read_only': False,
            'is_root_device': True,
            'path_on_host': '/tmp/example.ext4',
        }

    def test_create_network_interface(self, requests_mock):
        m = requests_mock.put(
            'http+unix://%2Ftmp%2Ftest.socket/network-interfaces/1')
        vm = Vm(0, '/tmp/test.socket')
        vm.create_network_interface(id=1)

        assert m.last_request.json() == {
            'guest_mac': '02:FC:00:00:00:00',
            'host_dev_name': 'fc-0-tap0',
            'id': 1,
            'iface_id': '1',
        }

    def test_create_snapshot(self, requests_mock):
        m = requests_mock.put(
            'http+unix://%2Ftmp%2Ftest.socket/snapshot/create')
        vm = Vm(0, '/tmp/test.socket')
        vm.create_snapshot('/tmp/foo', '/tmp/bar')

        assert m.last_request.json() == {
            "snapshot_type": "Full",
            "snapshot_path": '/tmp/foo',
            "mem_file_path": '/tmp/bar',
        }

    def test_load_snapshot(self, requests_mock):
        m = requests_mock.put(
            'http+unix://%2Ftmp%2Ftest.socket/snapshot/load')
        vm = Vm(0, '/tmp/test.socket')
        vm.load_snapshot('/tmp/foo', '/tmp/bar')

        assert m.last_request.json() == {
            "snapshot_path": '/tmp/foo',
            "mem_file_path": '/tmp/bar',
            "resume_vm": True
        }
