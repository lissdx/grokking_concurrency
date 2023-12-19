import socket
import os.path
import time
from threading import Thread, current_thread

SOCKET_FILE = "./mailbox"
BUFFER_SIZE = 1024


class Sender(Thread):
    def run(self) -> None:
        self.name = "Sender"
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(SOCKET_FILE)

        messages = ["Hello", " ", "world", "!"]
        for msg in messages:
            print(f"{current_thread().name}: Send: '{msg}'")
            client.sendall(str.encode(msg))

        client.close()


class Receiver(Thread):
    def run(self):
        self.name = "Receiver"
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.bind(SOCKET_FILE)
        server.listen()

        print(f"{current_thread().name}: Listening to incoming messages...")
        conn, addr = server.accept()

        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            message = data.decode()
            print(f"{current_thread().name}: Received: '{message}'")

        server.close()


def main() -> None:
    if os.path.exists(SOCKET_FILE):
        os.remove(SOCKET_FILE)

    receiver = Receiver()
    receiver.start()

    time.sleep(1)

    sender = Sender()
    sender.start()

    for thread in [receiver, sender]:
        thread.join()

    os.remove(SOCKET_FILE)


if __name__ == "__main__":
    main()
