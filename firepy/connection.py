from urllib.parse import quote_plus
import requests
import requests_unixsocket

requests_unixsocket.monkeypatch()


class Connection:
    _socket_path: str

    def __init__(self, socket_path: str):
        self._socket_path = 'http+unix://' + quote_plus(socket_path)

    def put(self, path, *args, **kwargs):
        response = requests.put(self._socket_path + path, *args, **kwargs)
        response.raise_for_status()
        return response
