#!/usr/bin/env python3
from ServerPckg.Server import Server
import time

if __name__ == "__main__":
    server = Server()
    server.connect()
    while not server.shutdown_flag:
        pass
    time.sleep(5)
