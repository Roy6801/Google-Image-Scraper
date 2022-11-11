from .arch import Master
from .scraped_response import ScrapedResponse
from multiprocessing import Value
from ctypes import c_bool, c_int, c_char
from tqdm import tqdm
import time


class Scraper(Master):

    def __init__(self, process_count=1):
        self.__process_count = process_count
        self.__null = b"_"
        self.__query = Value(c_char * 100, self.__null)
        self.__task = Value(c_bool, False)
        self.__at_work = Value(c_int, 0)
        self.__fun = Value(c_char * 100, self.__null)
        super().__init__(self.__query,
                         self.__task,
                         self.__at_work,
                         self.__fun,
                         worker_args="worker_args",
                         num_workers=process_count)

    def scrape(self,
               query,
               count=50,
               quality=False,
               progressbar=True,
               timeout=10):
        self.__timeout = timeout
        self.__urls = set()
        if self.__process_count > 1:
            print("\n[INFO] Gearing Up Quality Setting...\n")
            quality = True
        self.__query.value = query.encode("utf-8")
        self.__task.value = True
        if quality:
            self.__fun.value = b"high_res"
        else:
            self.__fun.value = b"low_res"

        self.__wait_till(at_work=self.__process_count)
        self.__fun.value = self.__null
        self.__progress_tracker(count, progressbar)
        self.__task.value = False
        self.__wait_till(at_work=0)
        self._flush_stream()

        return ScrapedResponse(query,
                               count,
                               len(self.__urls),
                               quality,
                               urls=list(self.__urls))

    def __progress_tracker(self, count, progressbar):
        output = self._output_stream()
        last_update = int(time.time())
        prev_len = len(self.__urls)
        curr_len = prev_len
        timed_out = False

        if progressbar:
            pbar = tqdm(total=count)
            pbar.set_description(f"Querying ({self.__query.value.decode()})")

        while curr_len < count:
            try:
                if curr_len == 1:
                    self.__fun.value = self.__null
                if not output.empty():
                    url = output.get()
                    self.__urls.add(url)
                    curr_len = len(self.__urls)
                    if curr_len > prev_len:
                        if progressbar: pbar.update(1)
                        last_update = int(time.time())
                    prev_len = curr_len
                elif int(time.time()) - last_update > self.__timeout:
                    timed_out = True
                    break
            except Exception as e:
                print(e)

        if progressbar: pbar.close()
        if timed_out: print("\n[INFO] Timeout! Moving on...\n")

    def __wait_till(self, at_work):
        while not self.__at_work.value == at_work:
            pass

    def close(self):
        self._stop_workers()

    def __del__(self):
        return super().__del__()
