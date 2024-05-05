import asyncio
import tracemalloc
import json
from pathlib import Path
from aioquic.asyncio import serve
from aioquic.quic.configuration import QuicConfiguration

FILE_PATH = "received_file.txt"
BUFFER_SIZE = 1024


def write_chunks_to_file(packets):
    try:
        # Open the file in write mode
        with open(FILE_PATH, 'w') as file:
            # Write each chunk to the file
            for key in range(len(packets)):
                file.write(packets[key])
        print("File created successfully.")
    except IOError as e:
        print(f"Error writing to file: {e}")


async def close_client(writer, packets):
    print("Sending eof to client...")
    writer.write_eof()
    await writer.drain()
    print("Stream closed.")

    write_chunks_to_file(packets)


async def receive_full_packet(reader):
    packet_data = b""
    packet_size = 0

    while True:
        data_chunk = await reader.read(BUFFER_SIZE - packet_size)
        if not data_chunk:
            # End of stream reached
            return None if packet_size == 0 else packet_data  # Return None if no data received, otherwise return received data

        packet_data += data_chunk
        packet_size = len(packet_data)

        if packet_size >= BUFFER_SIZE:
            # Received packet of size equal to or greater than BUFFER_SIZE
            return packet_data


async def decode_json_packet(reader):
    packet_data = await receive_full_packet(reader)
    if packet_data is None:
        return -1, "", "break"

    try:
        data_json = packet_data.decode('utf-8')
        data = json.loads(data_json)
        serial_num = data["serial_number"]
        packet_data = data["data"]

        if len(packet_data) < BUFFER_SIZE:
            return serial_num, packet_data, "break"

        return serial_num, packet_data, "continue"

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON data: {e}")
        return -1, "", "break"


async def handle_stream(reader, writer):
    packets = dict()
    print("New stream opened.")
    while True:
        serial_num, data, command = await decode_json_packet(reader)

        if serial_num != -1:
            packets[serial_num] = data

        if command == "break":
            break

    await close_client(writer, packets)


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
