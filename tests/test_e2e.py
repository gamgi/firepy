import pytest
from unittest.mock import Mock, patch
from firepy.firecracker import Firecracker

MOCK_IDS = ['id1', 'id2', 'id3']


@pytest.fixture(autouse=True)
def mock_uuid():
    with patch('firepy.firecracker.uuid4', side_effect=MOCK_IDS):
        yield


class TestE2E:
    def test_create_vm_calls_firecracker_binary_with_unique_socket(self):
        binary = Mock()
        fc = Firecracker(binary)
        fc.create_vm()

        binary.assert_called_with(**{
            '_bg_exc': True,
            'api-sock': '/tmp/firecracker-id1.socket'
        })
