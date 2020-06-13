from ServerPckg.Server import Server
import time
import keyboard

if __name__ == "__main__":
    server = Server()
    server.connect()
    while not server.shutdown_flag:
        if keyboard.is_pressed('q'):
            server.disconnect('\nServer closed!')
            break
    time.sleep(5)
