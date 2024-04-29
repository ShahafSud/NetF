import asyncio
import sys
import tracemalloc
from pathlib import Path
from aioquic.asyncio import serve
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration

time_sleep = int(sys.argv[2])  # Adjust as needed

# Enable tracemalloc
tracemalloc.start()


class EchoQuicProtocol(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quic_events = asyncio.Queue()

    async def quic_event_received(self, event):
        # Asynchronous sleep for the specified delay
        await asyncio.sleep(time_sleep)
        # Handle the event
        if isinstance(event, tuple):
            stream_id, data = event
            print(f"Received from client on stream {stream_id}: {data.decode()}")

    async def quic_event_handler(self):
        while True:
            # We'll directly await quic_event_received here
            await self.quic_event_received(await self.quic_events.get())

    def connection_made(self, transport):
        super().connection_made(transport)
        asyncio.ensure_future(self.quic_event_handler())

    def quic_stream_data_received(self, stream_id: int, data: bytes) -> None:
        asyncio.ensure_future(self.quic_event_received((stream_id, data)))

    def quic_connection_lost(self, exc: Exception) -> None:
        print("Connection lost with client.")


async def run_quic_server():
    configuration = QuicConfiguration(is_client=False)
    configuration.load_cert_chain(certfile=Path("certificate.pem"), keyfile=Path("key.pem"))

    server = await serve(
        host="127.0.0.1",
        port=int(sys.argv[1]),
        configuration=configuration,
        create_protocol=EchoQuicProtocol
    )

    # Keep the server running indefinitely
    try:
        await asyncio.Event().wait()
    finally:
        server.close()
        await server.close()


asyncio.run(run_quic_server())
