import asyncio
import tracemalloc
import pandas as pd
import sys
from aioquic.asyncio import connect, QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration

# Constants
BUFFER_SIZE = 4096
QUIC_PACKET_OVERHEAD = 30  # Adjust according to your QUIC implementation
TimeToWait = sys.argv[1]
FILE_PATH = "random_file.txt"


def divide_file_into_chunks():
    """
    Divides the file into chunks considering the QUIC packet overhead.

    Returns:
        List of byte chunks read from the file.
    """
    chunks = []
    with open(FILE_PATH, 'rb') as file:
        while True:
            data = file.read(BUFFER_SIZE - QUIC_PACKET_OVERHEAD)
            if not data:
                break  # Reached end of file
            chunks.append(data)
    return chunks


class CustomQuicConnectionProtocol(QuicConnectionProtocol):
    """
    Custom QUIC connection protocol with RTT (Round Trip Time) logging.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the CustomQuicConnectionProtocol.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.rtt_samples = pd.DataFrame(columns=["RTT", "Smoothed RTT"])

    async def send_chunks(self, reader, writer):
        """
        Sends file chunks over the QUIC connection and logs RTT metrics.

        Args:
            reader: Stream reader.
            writer: Stream writer.
        """
        chunks = divide_file_into_chunks()

        initial_rtt, initial_smoothed_rtt = self.log_rtt_metrics()

        for chunk in chunks:
            writer.write(chunk)
            await writer.drain()
            await reader.read(BUFFER_SIZE)
            rtt, smoothed_rtt = self.log_rtt_metrics()
            self.rtt_samples = self.rtt_samples._append(
                {"RTT": rtt, "Smoothed RTT": smoothed_rtt}, ignore_index=True
            )

        print("[FILE SENT SUCCESSFULLY]")
        print("Sending eof to server...", end="")
        self.save_rtts()
        print("RTTs Saved!")
        writer.write_eof()
        await writer.drain()
        await reader.read(BUFFER_SIZE)

    def log_rtt_metrics(self):
        """
        Logs the latest and smoothed RTT values.

        Returns:
            tuple: Latest RTT and smoothed RTT.
        """
        connection = self._quic
        rtt = connection._loss._rtt_latest
        smoothed_rtt = connection._loss._rtt_smoothed
        return rtt, smoothed_rtt

    def save_rtts(self):
        """
        Saves the RTT metrics to a CSV file.
        """
        self.rtt_samples.to_csv(f"CSV/RTTs_{TimeToWait}.csv")


async def run_client(host, port):
    """
    Runs the QUIC client.

    Args:
        host (str): Host address to connect to.
        port (int): Port number to connect to.
    """
    configuration = QuicConfiguration(is_client=True)
    configuration.verify_mode = False
    tracemalloc.start()

    async with connect(host, port, configuration=configuration,
                       create_protocol=CustomQuicConnectionProtocol) as protocol:
        print("Connecting to server...", end="")
        await protocol.wait_connected()
        reader, writer = await protocol.create_stream()
        print("Connected")

        await protocol.send_chunks(reader, writer)

        protocol.close()
        await protocol.wait_closed()

    tracemalloc.stop()


def main():
    """
    Main entry point for the script.
    """
    asyncio.run(run_client('localhost', 4433))


if __name__ == "__main__":
    main()
