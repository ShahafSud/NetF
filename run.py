import os
import server
import client

def main():
    port = 54000
    end = 11 # 101
    for i in range(0, end, 5):
        server.main(str(port+i), str(i))
        client.main(str(port+i), str(i))
    # for i in range(0, end, 5):
    #     os.system(f"python3 plotting.py {i}")


if __name__ == '__main__':
    main()