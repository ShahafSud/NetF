import asyncio
import sys
import tracemalloc
import time
from aioquic.asyncio import connect
from aioquic.quic.configuration import QuicConfiguration

FILE_PATH = "random_file.txt"
BUFFER_SIZE = 4096

# Adjust BUFFER_SIZE to account for QUIC packet overhead
QUIC_PACKET_OVERHEAD = 30  # Adjust this value according to your QUIC implementation

time_to_wait = sys.argv[1]


def divide_file_into_chunks():
    chunks = []
    with open(FILE_PATH, 'rb') as file:
        while True:
            data = file.read(BUFFER_SIZE - QUIC_PACKET_OVERHEAD)  # Adjust buffer size
            if not data:
                break  # Reached end of file
            chunks.append(data)
    return chunks


async def send_chunks(reader, writer):
    chunks = divide_file_into_chunks()
    rtt_list = []

    for chunk in chunks:
        start_time = time.time()
        writer.write(chunk)
        await writer.drain()
        end_time = time.time()
        rtt_list.append(end_time - start_time)

    print("[FILE SENT SUCCESSFULLY]")
    print("Sending eof to server...", end="")
    writer.write_eof()
    await writer.drain()
    await reader.read(BUFFER_SIZE)

    return rtt_list


async def run_client(host, port):
    configuration = QuicConfiguration(is_client=True)
    configuration.verify_mode = False
    tracemalloc.start()

    async with connect(host, port, configuration=configuration) as protocol:
        print("Connecting to server...", end="")
        await protocol.wait_connected()
        reader, writer = await protocol.create_stream()
        print("Connected")

        RTT_list = await send_chunks(reader, writer)

        protocol.close()
        await protocol.wait_closed()

    print("\n" + str(len(RTT_list)))


def main():
    asyncio.run(run_client('localhost', 4433))
    tracemalloc.stop()


if __name__ == "__main__":
    main()
