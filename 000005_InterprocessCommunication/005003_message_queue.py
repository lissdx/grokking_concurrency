import time
from queue import Queue
from threading import Thread, current_thread


class Worker(Thread):

    def __init__(self, q: Queue, w_id: int):
        super().__init__(name=str(w_id))
        self.queue = q

    def run(self) -> None:
        while not self.queue.empty():
            item = self.queue.get()
            print(f"Thread {current_thread().name}: "f"processing item {item} from the queue")
            time.sleep(2)


def main(threadNum: int) -> None:
    q = Queue()
    for i in range(10):
        q.put(i)

    threads = []
    for i in range(threadNum):
        thread = Worker(q, i + 1)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    thread_num = 4
    main(thread_num)
