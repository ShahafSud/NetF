import asyncio
from aioquic.asyncio import serve
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
import sys
import time

class EchoQuicProtocol(QuicConnectionProtocol):
    def quic_event_received(self, event):
        time.sleep(time_sleep)  # Sleep for the specified delay

time_sleep = int(sys.argv[2]) * 0.001  # Convert input from milliseconds to seconds

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
    await server.wait_closed()

asyncio.run(run_quic_server())
