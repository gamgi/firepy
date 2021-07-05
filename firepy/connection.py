import requests
import requests_unixsocket

requests_unixsocket.monkeypatch()


class Connection:
    _socket_path: str

    def __init__(self, socket_path: str):
        self._socket_path = socket_path
