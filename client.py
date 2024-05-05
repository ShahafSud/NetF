import asyncio
import sys
import tracemalloc
import json
import time
from aioquic.asyncio import connect
from aioquic.quic.configuration import QuicConfiguration

FILE_PATH = "random_file.txt"
BUFFER_SIZE = 1024

# Adjust BUFFER_SIZE to account for QUIC packet overhead
QUIC_PACKET_OVERHEAD = 20  # Adjust this value according to your QUIC implementation

time_to_wait = sys.argv[1]


def create_json_packet(data, serial_number):
    """
    Create a JSON packet with specified data and serial number.
    """
    packet = {
        "serial_number": serial_number,
        "data": data
    }
    json_packet = json.dumps(packet)
    return json_packet


def divide_file_into_packets():
    packets = []
    with open(FILE_PATH, 'r') as file:
        while True:
            data = file.read(BUFFER_SIZE - QUIC_PACKET_OVERHEAD)  # Adjust buffer size
            if not data:
                break  # Reached end of file
            packet = create_json_packet(data, len(packets))
            packets.append(packet)
    return packets


async def send_file_loop(reader, writer):
    data_packets = divide_file_into_packets()
    rtt_list = []

    for packet in data_packets:
        start_time = time.time()
        await send_packet(writer, reader, packet)
        end_time = time.time()
        rtt_list.append(end_time - start_time)

    print("[FILE SENT SUCCESSFULLY]")
    print("Sending eof to server...", end="")
    writer.write_eof()
    await reader.read(BUFFER_SIZE)

    return rtt_list


async def send_packet(writer, reader, packet):
    packet_size = len(packet)
    offset = 0

    while offset < packet_size:
        end_offset = min(offset + BUFFER_SIZE, packet_size)
        packet_part = packet[offset:end_offset]
        writer.write(packet_part.encode("utf-8"))  # Encode chunk to bytes before sending
        await writer.drain()
        offset = end_offset


async def run_client(host, port):
    configuration = QuicConfiguration(is_client=True)
    configuration.verify_mode = False
    tracemalloc.start()

    async with connect(host, port, configuration=configuration) as protocol:
        print("Connecting to server...", end="")
        await protocol.wait_connected()
        reader, writer = await protocol.create_stream()
        print("Connected")

        RTT_list = await send_file_loop(reader, writer)

        protocol.close()
        await protocol.wait_closed()

    print("\n" + str(len(RTT_list)))


def main():
    asyncio.run(run_client('localhost', 4433))
    tracemalloc.stop()


if __name__ == "__main__":
    main()
