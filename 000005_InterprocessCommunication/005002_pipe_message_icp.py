import time
from threading import Thread, current_thread
from multiprocessing import Pipe
from multiprocessing.connection import Connection

STOP = False


class Writer(Thread):
    def __init__(self, conn: Connection):
        super().__init__()
        self.connection = conn
        self.name = "Writer"

    def run(self) -> None:
        for i in range(5):
            time.sleep(2)
            print(f"{current_thread().name}: Sending rubber duck...")
            self.connection.send(f"Rubber duck:{i}")


class Reader(Thread):
    def __init__(self, conn: Connection, name: str):
        super().__init__()
        self.connection = conn
        # self.name = "Reader"
        self.name = name

    def run(self) -> None:
        msg_count = 0
        while msg_count < 5:
            time.sleep(1)
            print(f"{current_thread().name}: Reading...")
            msg = self.connection.recv()
            print(f"{current_thread().name}: Received: {msg}")
            msg_count += 1

    # def run(self) -> None:
    #     # msg_count = 0
    #     while not STOP:
    #         time.sleep(1)
    #         print(f"{current_thread().name}: Reading...")
    #         # msg = self.connection.recv()
    #         if self.connection.poll(timeout=1.0):
    #             msg = self.connection.recv()
    #             print(f"{current_thread().name}: Received: {msg}")
    #         # msg = self.connection.poll(timeout=1.0)
    #         # msg_count += 1


def main() -> None:
    reader_conn, writer_conn = Pipe()

    reader1 = Reader(reader_conn, "Reader_1")
    # reader2 = Reader(reader_conn, "Reader_2")
    writer = Writer(writer_conn)

    threads = [writer, reader1]

    for thread in threads:
        thread.start()

    time.sleep(10)

    global STOP
    STOP = True

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
