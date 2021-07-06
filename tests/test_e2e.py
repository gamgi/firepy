import pytest
from unittest.mock import Mock, patch, ANY
from firepy.firecracker import Firecracker

MOCK_IDS = ['id1', 'id2', 'id3']


@pytest.fixture(autouse=True)
def mock_uuid():
    with patch('firepy.firecracker.uuid4', side_effect=MOCK_IDS):
        yield


class TestE2E:
    def test_create_vm_calls_firecracker_binary_with_unique_socket(self):
        binary = Mock()
        Firecracker(binary).create_vm()

        binary.assert_called_with(
            '--api-sock', '/tmp/firecracker-id1.socket',
            **{'_bg': True, '_err': ANY}
        )

    def test_start_vm_calls_firecracker_api(self, requests_mock):
        m = requests_mock.put(
            'http+unix://%2Ftmp%2Ffirecracker-id1.socket/actions')

        fc = Firecracker(Mock())
        fc.create_vm().start()

        assert m.last_request.json() == {'action_type': 'InstanceStart'}
        assert m.last_request.scheme == 'http+unix'
