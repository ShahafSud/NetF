# client.py
import asyncio
import sys
import time
import tracemalloc
from aioquic.asyncio import connect
from aioquic.quic.configuration import QuicConfiguration


async def run_client(host, port):
    configuration = QuicConfiguration(is_client=True)
    configuration.verify_mode = False
    tracemalloc.start()

    async with connect(host, port, configuration=configuration) as protocol:
        print("Connecting to server...", end="")
        await protocol.wait_connected()
        reader, writer = await protocol.create_stream()
        print("Connected")

        while not reader.at_eof():
            text = sys.argv[1]#input("Message: ")
            Stime = time.time()
            writer.write(text.encode())
            print("Sending to server...", end="")
            await reader.read(1024)
            Etime = time.time()
            print("RTT was : " + str(Etime-Stime))

        print("done")
        print("Sending eof...", end="")
        writer.write_eof()
        protocol.close()
        await protocol.wait_closed()
        print("done")


def main():
    asyncio.run(run_client('localhost', 4433))
    tracemalloc.stop()


if __name__ == "__main__":
    main()
