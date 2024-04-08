Auther: Shahaf Sudai

README

Before running the code in this repository please run:

1)
pip install aioquic

2)
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out certificate.pem -days 365 -nodes -subj "/CN=localhost"
this command will create two files.
DO NOT ADD them to the git repository during work and commits!

The commands for run are:

python3 server.py <server_port> <sleep_time_in_ms> (recommended port : )

python3 client.py <client_port> (recommended port : )