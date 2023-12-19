import time
import queue
import typing as T
from threading import Thread, current_thread

Callback = T.Callable[..., None]
Task = T.Tuple[Callback, T.Any, T.Any]
TaskQueue = queue.Queue


class Worker(Thread):
    def __init__(self, tasks: queue.Queue[Task]):
        super().__init__()
        self.tasks = tasks

    def run(self) -> None:
        while True:
            func, ars, kargs = self.tasks.get()
            try:
                func(*ars, **kargs)
            except Exception as e:
                print(e)
            self.tasks.task_done()


class ThreadPool:
    def __init__(self, numTreads: int):
        self.tasks: TaskQueue = queue.Queue(numTreads)
        self.num_threads = numTreads

        for _ in range(self.num_threads):
            worker = Worker(self.tasks)
            worker.setDaemon(True)
            worker.start()

    def submit(self, func: Callback, *args, **kwargs) -> None:
        self.tasks.put((func, args, kwargs))

    def wait_competition(self) -> None:
        self.tasks.join()


def cpu_waster(i: int) -> None:
    name = current_thread().getName()
    print(f"{name} doing {i} work")
    time.sleep(3)


def main() -> None:
    pool = ThreadPool(numTreads=5)
    for i in range(20):
        pool.submit(cpu_waster, i)

    print("All work requests sent")
    pool.wait_completion()
    print("All work completed")


if __name__ == "__main__":
    main()
