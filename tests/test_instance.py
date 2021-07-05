from firepy.instance import Instance


class TestInstance:
    def test_start_vm(self, requests_mock):
        m = requests_mock.put('unix:///tmp/test.socket')

        vm = Instance('/tmp/test.socket')
        vm.start()

        assert m.last_request.json() == {'action_type': 'InstanceStart'}
        assert m.last_request.scheme == 'unix'

    def test_set_rootfs(self, requests_mock):
        m = requests_mock.put('unix:///tmp/test.socket')
        vm = Instance('/tmp/test.socket')
        vm.set_rootfs('/tmp/example.ext4')

        assert m.last_request.json() == {
            'drive_id': 'rootfs',
            'is_read_only': False,
            'is_root_device': True,
            'path_on_host': '/tmp/example.ext4',
        }
        assert m.last_request.scheme == 'unix'
