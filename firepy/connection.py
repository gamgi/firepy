from urllib.parse import quote
import requests
import requests_unixsocket

requests_unixsocket.monkeypatch()


class Connection:
    _socket_path: str

    def __init__(self, socket_path: str):
        self._socket_path = 'unix://' + quote(socket_path)

    def put(self, *args, **kwargs):
        return requests.put(self._socket_path, *args, **kwargs)
