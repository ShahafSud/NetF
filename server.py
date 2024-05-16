import asyncio
import time
import tracemalloc
from pathlib import Path
from aioquic.asyncio import serve
from aioquic.quic.configuration import QuicConfiguration

time_to_wait = 0
FILE_PATH = "received_file.txt"
BUFFER_SIZE = 4096
async def write_chunks_to_file(packets):
    try:
        # Open the file in write mode
        with open(FILE_PATH, 'wb') as file:
            # Write each chunk to the file
            for packet in packets:
                file.write(packet)
        print("File created successfully.")
    except IOError as e:
        print(f"Error writing to file: {e}")


async def close_client(writer, packets):
    print("Sending eof to client...")
    writer.write_eof()
    await writer.drain()
    print("Stream closed.")

    await write_chunks_to_file(packets)


async def handle_stream(reader, writer):
    packets = []
    print("New stream opened.")
    try:
        while True:
            data_chunk = await reader.read(BUFFER_SIZE)
            time.sleep(time_to_wait)
            writer.write(data_chunk)
            if not data_chunk:
                # End of stream reached
                break
            packets.append(data_chunk)

    finally:
        await close_client(writer, packets)


async def run_server(host, port):
    configuration = QuicConfiguration(is_client=False)
    configuration.load_cert_chain(certfile=Path("certificate.pem"), keyfile=Path("key.pem"))

    def handle_stream_awaited(reader, writer):
        asyncio.create_task(handle_stream(reader, writer))

    await serve(host, port, configuration=configuration, stream_handler=handle_stream_awaited)


def main(port, tts):
    global time_to_wait
    time_to_wait = int(tts)/1000
    tracemalloc.start()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run_server('localhost', port))
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
        tracemalloc.stop()


if __name__ == "__main__":
    main()
