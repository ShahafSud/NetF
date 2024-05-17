# QUIC File Transfer Project

This project demonstrates a simple file transfer application using the QUIC (Quick UDP Internet Connections) protocol. The project includes three main components:

1. **Client (`client.py`)**: Sends a file to the server in chunks and logs Round Trip Time (RTT) metrics.
2. **Server (`server.py`)**: Receives the file chunks from the client and writes them to a file.
3. **Plotting (`plotting.py`)**: Generates a plot of the RTT metrics collected during the file transfer.
4. **Random_File.txt (`random_file.txt`)**: random txt file in size 6MB ready to be sent.


## Table of Contents

- [Introduction](#introduction)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Usage](#usage)
  - [Server](#server)
  - [Client](#client)
  - [Plotting](#plotting)
  - [Random_File](#random_file)
- [Code Explanation](#code-explanation)
  - [Client](#client-1)
  - [Server](#server-1)
  - [Plotting](#plotting-1)
- [Unit Testing](#unit-testing)
  - [Client](#client-2)
  - [Server](#server-2)
  - [Plotting](#plotting-2)
- [Conclusion](#conclusion)

## Introduction

The project aims to demonstrate file transfer over a QUIC connection, a modern transport layer network protocol designed to provide low-latency connections. It also includes RTT measurement to analyze the performance of the connection.

## Project Structure
.
├── client.py
├── server.py
├── randomServer.py
├── plotting.py
├── random_file.txt
├── certificate.pem
├── key.pem
├── CSV
│ └── RTTs_<TimeToWait>.csv
└── plots
└── RTTs_<FILE_NAME>.png


- `client.py`: Sends a file to the server and logs RTT metrics.
- `server.py`: Receives the file from the client, waits a given time and returns it to the client.
- `randomServer.py`: Receives the file from the client, waits a random time for each chunk and returns it to the client.
- `plotting.py`: Plots the RTT metrics.
- `random_file.txt`: Example file to be transferred.
- `certificate.pem` and `key.pem`: SSL/TLS certificates for secure connection.
- `CSV`: Directory for storing RTT logs.
- `plots`: Directory for storing RTT plots.

## Dependencies

Ensure you have the following dependencies installed:

- Python 3.7+
- `aioquic`
- `pandas`
- `matplotlib`

You can install the required Python packages using pip:

```sh
pip install aioquic pandas matplotlib
```

Note, to compleat the setup run:
```sh
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out certificate.pem -days 365 -nodes -subj "/CN=localhost"
```

## Usage

### Server
Start the QUIC server with a specified delay (in milliseconds) to simulate network conditions:
```sh
python3 server.py <TimeToWait>
```
#### Example:
```sh
python3 server.py 100  # Introduces a 100ms delay
```
Or start the random server for random TimeToWait values (0 to 100 ms) with:
```sh
python3 randomServer.py
```

### Client
Start the QUIC client with the same delay parameter used by the server:
```sh
python3 client.py <TimeToWait>
```
#### Example:
```sh
python3 client.py 100  # Introduces a 100ms delay
```

### Plotting
Generate the RTT plot from the RTT logs collected during the file transfer:
```sh
python3 plotting.py <TimeToWait>
```

#### Example:
```sh
python3 plotting.py 100
```
The plot will be saved in the plots directory as RTTs_100.png.

### Random_file
The Random file is a txt file in size 6(MB) ready to be sent.

## Code-Explanation

### Client
The client (client.py) performs the following tasks:

1. File Division: Reads a file and divides it into chunks, considering the QUIC packet overhead.
2. Custom QUIC Protocol: Implements a custom QUIC protocol that logs RTT metrics.
3. Sending Chunks: Sends the file chunks to the server, logs the RTT for each chunk, and saves the RTT data to a CSV file.

### Server
The server (server.py) performs the following tasks:

1. Stream Handling: Handles incoming data streams from the client.
2. Simulate Delay: Introduces a configurable delay to simulate network conditions.
3. File Writing: Writes the received file chunks to a file.

### Plotting
The plotting script (plotting.py) performs the following tasks:

1. Load RTT Data: Reads RTT metrics from a CSV file.
2. Plotting: Plots the RTT and Smoothed RTT values using Matplotlib.
3. Save Plot: Saves the generated plot as a PNG file.

## Conclusion
This project showcases a basic implementation of a file transfer application using the QUIC protocol. It includes functionality to measure and plot RTT metrics, providing insights into the performance of the QUIC connection under various network conditions. This setup can be expanded and customized for more complex use cases and performance analyses.

## Unit Testing

### Client
The client component is tested using the following unit test:

test_file_division: Tests the behavior of the divide_file_into_chunks function. It verifies that the function correctly divides a file into chunks of the specified buffer size.

### Server
The server component is tested using the following unit test:

test_handle_stream: Tests the behavior of the handle_stream function. It verifies that the function correctly processes data chunks received from the client.

### Random Server
The same as server with a random time to wait for each chunk.

### Plotting
The plotting component is tested using the following unit test:

test_plotting: Tests the behavior of the main function in generating a plot. It verifies that the main function correctly generates a plot with RTT data loaded from a mock CSV file.