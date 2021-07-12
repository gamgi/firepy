from unittest.mock import Mock, ANY
from firepy.firecracker import Firecracker


class TestE2E:
    def test_create_vm_calls_firecracker_binary_with_unique_socket(self):
        binary = Mock()
        Firecracker(binary).create_vm()

        binary.assert_called_with(
            '--api-sock', '/tmp/firecracker-0.socket',
            **{'_bg': True, '_err': ANY, '_out': None, '_in': None}
        )

    def test_start_vm_calls_firecracker_api(self, requests_mock):
        m = requests_mock.put(
            'http+unix://%2Ftmp%2Ffirecracker-0.socket/actions')

        fc = Firecracker(Mock())
        fc.create_vm().start()

        assert m.last_request.json() == {'action_type': 'InstanceStart'}
        assert m.last_request.scheme == 'http+unix'
