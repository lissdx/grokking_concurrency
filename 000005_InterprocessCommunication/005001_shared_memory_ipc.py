import time
from threading import Thread, current_thread

SIZE = 5
shared_memory = [-1] * SIZE


class Producer(Thread):
    def run(self) -> None:
        self.name = "Producer"
        global shared_memory
        for i in range(SIZE):
            time.sleep(1)
            print(f"{current_thread().name}: Writing {int(i)}")
            shared_memory[i - 1] = i


class Consumer(Thread):
    def run(self) -> None:
        self.name = "Consumer"
        global shared_memory
        for i in range(SIZE):
            while True:
                line = shared_memory[i]
                if line == -1:
                    print(f"{current_thread().name}: Data not available\n" f"Sleeping for 1 second before retrying")
                    time.sleep(1)
                    continue
                print(f"{current_thread().name}: Read: {int(line)}")
                break


def main() -> None:
    threads = [Consumer(), Producer()]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
