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
            # self._send_ping()

        elif hasattr(event, 'packet_received') and event.packet_received:
            # A packet (could be our ping response) is received
            end_time = time.time()
            if self.start_time:
                rtt = end_time - self.start_time
                print(f"RTT measured: {rtt:.3f} seconds")
                self.start_time = None  # Reset start time

    def _send_ping(self):
        self._quic.send_ping(uid=int(self.start_time * 1000))


async def run_quic_client():
    configuration = QuicConfiguration(is_client=True)
    configuration.verify_mode = False  # For demo purposes only
    tracemalloc.start()

    async with connect(
            host='127.0.0.1',
            port=int(sys.argv[1]),
            configuration=configuration,
            create_protocol=EchoQuicProtocol
    ):
        # No need to await anything here, connection will be closed when exiting the block
        await asyncio.sleep(1000)
        print("Done")


asyncio.run(run_quic_client())
