from multiprocessing import Process, Queue, Value
from ctypes import c_bool
from . import jobs
import time
import math


class _Worker(Process):

    def __init__(self, *args):
        super().__init__()
        # queue, pid, query, task, fun, worker_args, alive
        self.__p_id, self.__num, self.__output_queue, *self.__params, self.__alive = args

    def run(self):
        *args, fun, worker_args = self.__params
        worker_init = getattr(jobs, worker_args)
        task_args = *worker_init(), *args

        while self.__alive.value:
            try:
                if fun.value != b"_":
                    work = getattr(jobs, fun.value.decode())
                    if hasattr(work, "__call__"):
                        work(self.__p_id, self.__num, self.__output_queue,
                             *task_args)
            except Exception as e:
                print(e)
            finally:
                time.sleep(1)


class Master:

    def __init__(self, *args, worker_args="worker_args", num_workers=1):
        self.__num = num_workers
        self.__output_queue = Queue()
        self.__alive = Value(c_bool, True)
        self.__params = *args, worker_args
        self.__call_workers()

    def __call_workers(self):
        self.__workers = [
            _Worker(pid, self.__num, self.__output_queue, *self.__params,
                    self.__alive) for pid in range(self.__num)
        ]

        for worker in self.__workers:
            worker.start()

        time.sleep(self.__init_time())

    def __init_time(self):
        interval = round(self.__num / math.pi, 2)
        return interval

    def _output_stream(self):
        return self.__output_queue

    def _flush_stream(self):
        time.sleep(0.5)
        while not self.__output_queue.empty():
            self.__output_queue.get()

    def _stop_workers(self):
        self.__alive.value = False

        for worker in self.__workers:
            worker.join()

    def __del__(self):
        self._stop_workers()
