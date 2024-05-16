import asyncio
import sys
import time
import tracemalloc
from pathlib import Path
from aioquic.asyncio import serve
from aioquic.quic.configuration import QuicConfiguration

# Get the time to wait from command-line arguments and convert to seconds
time_to_wait = int(sys.argv[1]) / 1000

# Constants for file path and buffer size
FILE_PATH = "received_file.txt"
BUFFER_SIZE = 4096


async def write_chunks_to_file(packets):
    """
    Writes the collected packets to a file.

    Args:
        packets (list of bytes): List of data packets to write to the file.
    """
    try:
        with open(FILE_PATH, 'wb') as file:
            for packet in packets:
                file.write(packet)
        print("File created successfully.")
    except IOError as e:
        print(f"Error writing to file: {e}")


async def close_client(writer, packets):
    """
    Closes the client connection and writes the packets to a file.

    Args:
        writer (StreamWriter): The stream writer for the client connection.
        packets (list of bytes): List of data packets received from the client.
    """
    print("Sending eof to client...")
    writer.write_eof()
    await writer.drain()
    print("Stream closed.")

    await write_chunks_to_file(packets)


async def handle_stream(reader, writer):
    """
    Handles the data stream from the client.

    Args:
        reader (StreamReader): The stream reader for the client connection.
        writer (StreamWriter): The stream writer for the client connection.
    """
    packets = []
    print("New stream opened.")
    try:
        while True:
            data_chunk = await reader.read(BUFFER_SIZE)
            time.sleep(time_to_wait)  # Simulate delay
            writer.write(data_chunk)
            if not data_chunk:
                break  # End of stream reached
            packets.append(data_chunk)
    finally:
        await close_client(writer, packets)


async def run_server(host, port):
    """
    Runs the QUIC server.

    Args:
        host (str): The hostname or IP address to bind the server to.
        port (int): The port number to bind the server to.
    """
    configuration = QuicConfiguration(is_client=False)
    configuration.load_cert_chain(certfile=Path("certificate.pem"), keyfile=Path("key.pem"))

    def handle_stream_awaited(reader, writer):
        asyncio.create_task(handle_stream(reader, writer))

    await serve(host, port, configuration=configuration, stream_handler=handle_stream_awaited)


def main():
    """
    Main entry point for the server application.
    """
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
