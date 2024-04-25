import asyncio
from aioquic.asyncio import serve
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
import sys

time_sleep = int(sys.argv[2]) * 0.001  # Convert input from milliseconds to seconds


class EchoQuicProtocol(QuicConnectionProtocol):
    async def quic_event_received(self, event):
        # Asynchronous sleep for the specified delay
        await asyncio.sleep(time_sleep)


async def run_quic_server():
    configuration = QuicConfiguration(is_client=False)
    configuration.load_cert_chain(certfile="certificate.pem", keyfile="key.pem")

    server = await serve(
        host='127.0.0.1',
        port=int(sys.argv[1]),
        configuration=configuration,
        create_protocol=EchoQuicProtocol
    )

    # Keep the server running indefinitely
    await asyncio.Event().wait()


asyncio.run(run_quic_server())
