# server.py
import asyncio
import time
import tracemalloc
from pathlib import Path
from aioquic.asyncio import serve
from aioquic.quic.configuration import QuicConfiguration
async def handle_stream(reader, writer):
    print("New stream opened.")
    data = await reader.read(1024)
    while not reader.at_eof():
        print(f"Received instruction to wait: {data.decode()} Mili-Sec.")
        time.sleep(int(data.decode())*0.001)
        writer.write_eof()
        data = await reader.read(1024)
    print("Stream closed.")


async def run_server(host, port):
    configuration = QuicConfiguration(is_client=False)

    configuration.load_cert_chain(certfile=Path("certificate.pem"), keyfile=Path("key.pem"))

    def handle_stream_awaited(reader, writer):
        asyncio.create_task(handle_stream(reader, writer))

    await serve(host, port, configuration=configuration, stream_handler=handle_stream_awaited)


def main():
    tracemalloc.start()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run_server('localhost', 4433))
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()

    tracemalloc.stop()


if __name__ == "__main__":
    main()
