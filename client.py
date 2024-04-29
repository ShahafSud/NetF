import asyncio
import time
import tracemalloc
from aioquic.asyncio import connect
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import HandshakeCompleted
import sys


class EchoQuicProtocol(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_time = None  # Record the time when data is sent

    def quic_event_received(self, event):
        if isinstance(event, HandshakeCompleted):
            # Handshake completed, now safe to send data
            print("Client has been connected successfully to server in port " + sys.argv[1])
            self.start_time = time.time()  # Update start time

    async def send_user_input(self):
        while True:
            user_input = input("Enter message to send to server (type 'quit' to exit): ")
            if user_input.lower() == 'quit':
                break
            print("data has been sent.\n")
            self._quic.send_stream_data(stream_id=0, data=user_input.encode())

    
    def quic_stream_data_received(stream_id: int, data: bytes) -> None:
        print(f"Received from server on stream {stream_id}: {data.decode()}")

    
    def quic_connection_lost(exc: Exception) -> None:
        print("Connection lost.")
        asyncio.get_event_loop().stop()


async def run_quic_client():
    configuration = QuicConfiguration(is_client=True)
    configuration.verify_mode = False  # For demo purposes only
    tracemalloc.start()

    async with connect(
            host='127.0.0.1',
            port=int(sys.argv[1]),
            configuration=configuration,
            create_protocol=EchoQuicProtocol
    ) as protocol:
        await protocol.send_user_input()


asyncio.run(run_quic_client())
