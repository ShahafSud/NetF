import asyncio
import time
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
            self.start_time = time.time()  # Update start time
            self._quic.send_ping()  # Sending a ping to measure RTT

        elif event.packet_received:
            # A packet (could be our ping response) is received
            end_time = time.time()
            if self.start_time:
                rtt = end_time - self.start_time
                print(f"RTT measured: {rtt:.3f} seconds")
                self.start_time = None  # Reset start time

async def run_quic_client():
    configuration = QuicConfiguration(is_client=True)
    configuration.verify_mode = False  # For demo purposes only

    async with connect(
        host='127.0.0.1',
        port=int(sys.argv[1]),
        configuration=configuration,
        create_protocol=EchoQuicProtocol
    ) as protocol:
        await protocol.wait_closed()  # Wait for the connection to close

asyncio.run(run_quic_client())
