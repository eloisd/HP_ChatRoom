import io

from dvic_chat.protocol import DataStream

class FakeSocket:

    def __init__(self) -> None:
        self.buffer = io.BytesIO()

    def send(self, b: bytes):
        self.buffer.write(b)

    def recv(self, size: int) -> bytes:
        self.buffer.seek(0)
        return self.buffer.read(size)
    
def test_receive_int():
    fs = FakeSocket()
    fs.send(b'\x00\x00\x00*') # 42 in bytes

    ds = DataStream(fs)
    assert ds.receive_int() == 42

def test_send_int():
    fs = FakeSocket()

    ds = DataStream(fs)
    ds.send_int(42)
    fs.buffer.seek(0)
    assert fs.buffer.read() == b'\x00\x00\x00*'
