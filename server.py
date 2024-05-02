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
            for key in range(len(packets.keys())):
                file.write(packets[key])
        print("File created successfully.")
    except IOError as e:
        print(f"Error writing to file: {e}")


async def close_client(writer, packets):
    print("Sending eof to client...")
    writer.write_eof()
    await writer.drain()
    """
    print("Chunks received:")
    for key in range(len(packets.keys())):
        print(f"[CHUNK {key}] | {packets[key]}\n")
    """
    print("Stream closed.")

    write_chunks_to_file(packets)


async def read_packet(reader, data_json):
    data_json = data_json.decode('utf-8')
    packet_size = len(data_json)

    while packet_size < BUFFER_SIZE:
        data_remains = BUFFER_SIZE - packet_size

        additional_data = await reader.read(data_remains)
        print("additional data: " + str(additional_data.decode('utf-8')))
        data_json += additional_data.decode('utf-8')
        packet_size = len(data_json)

    try:
        print(f"Complete data length: {packet_size}")
        print(f"Complete data: {data_json}")
        data = json.loads(data_json)
        print(data)
        serial_num = data["serial_number"]
        packet_size = data["size"]
        # time_to_wait = data["sleep"]
        packet_data = data["data"]

        if packet_size < BUFFER_SIZE:
            return serial_num, packet_data, "break"

        return serial_num, packet_data, "continue"

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON data: {e}")
        return -1, "", "break"


async def handle_stream(reader, writer):
    packets = dict()
    print("New stream opened.")
    while True:
        data_json = await reader.read(BUFFER_SIZE)
        if not data_json:
            break  # If no data is received, exit the loop
        # print(data_json.decode("utf-8") + "\n")

        serial_num, data, command = await read_packet(reader, data_json)

        if serial_num != -1:
            ack = "ack".encode("utf-8")
            writer.write(ack)

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
