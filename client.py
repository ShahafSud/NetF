import asyncio
import tracemalloc
from aioquic.asyncio import connect, QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
import pandas as pd

FILE_PATH = "random_file.txt"
BUFFER_SIZE = 4096
# Adjust BUFFER_SIZE to account for QUIC packet overhead
QUIC_PACKET_OVERHEAD = 30  # Adjust this value according to your QUIC implementation
TimeToWait = ""



def divide_file_into_chunks():
    chunks = []
    with open(FILE_PATH, 'rb') as file:
        while True:
            data = file.read(BUFFER_SIZE - QUIC_PACKET_OVERHEAD)  # Adjust buffer size
            if not data:
                break  # Reached end of file
            chunks.append(data)
    return chunks


class CustomQuicConnectionProtocol(QuicConnectionProtocol):  # a decorator over the library protocol
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rtt_samples = pd.DataFrame(columns=["RTT", "Smoothed RTT"])
    async def send_chunks(self, reader, writer):
        chunks = divide_file_into_chunks()

        initial_rtt, initial_smoothed_rtt = self.log_rtt_metrics()
        print(f"Initial RTT: {initial_rtt}, Initial Smoothed RTT: {initial_smoothed_rtt}")

        for chunk in chunks:
            writer.write(chunk)
            await writer.drain()
            await reader.read(BUFFER_SIZE)
            rtt, smoothed_rtt = self.log_rtt_metrics()
            self.rtt_samples = self.rtt_samples._append({"RTT": rtt, "Smoothed RTT": smoothed_rtt}, ignore_index=True)

        print("[FILE SENT SUCCESSFULLY]")
        print("Sending eof to server...", end="")
        self.saveRTTs()
        print("RTTs Saved!")
        writer.write_eof()
        await writer.drain()
        await reader.read(BUFFER_SIZE)

    def log_rtt_metrics(self):
        connection = self._quic
        rtt = connection._loss._rtt_latest
        smoothed_rtt = connection._loss._rtt_smoothed
        return rtt, smoothed_rtt


    def saveRTTs(self):
        self.rtt_samples.to_csv("CSV/RTTs_" + TimeToWait + ".csv")

async def run_client(host, port):
    configuration = QuicConfiguration(is_client=True)
    configuration.verify_mode = False
    tracemalloc.start()

    async with connect(host, port, configuration=configuration, create_protocol=CustomQuicConnectionProtocol) as protocol:
        print("Connecting to server...", end="")
        await protocol.wait_connected()
        reader, writer = await protocol.create_stream()
        print("Connected")

        await protocol.send_chunks(reader, writer)

        protocol.close()
        await protocol.wait_closed()



def main(port, tts):
    global TimeToWait
    TimeToWait = tts
    asyncio.run(run_client('localhost', port))
    tracemalloc.stop()


if __name__ == "__main__":
    main()
