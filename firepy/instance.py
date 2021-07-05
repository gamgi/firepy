from firepy.connection import Connection


class Instance:
    conn: Connection

    def __init__(self, socket_path: str):
        self.conn = Connection(socket_path)

    def start(self):
        pass

    def pause(self):
        pass

    def set_kernel(self):
        pass

    def set_rootfs(self):
        pass
