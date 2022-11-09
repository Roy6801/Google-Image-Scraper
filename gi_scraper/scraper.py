'''Scraper class extends Master class. Default is
low quality scraping unlesss passed quality=True.
For processes > 1, quality=True by default.'''

from arch import Master
from scraped_response import ScrapedResponse
from multiprocessing import Value
from ctypes import c_bool, c_char
from tqdm import tqdm
import time


class Scraper(Master):

    def __init__(self, process_count=1):
        self.__process_count = process_count
        self.__null = b"_"
        self.__query = Value(c_char * 100, self.__null)
        self.__task = Value(c_bool, False)
        self.__fun = Value(c_char * 100, self.__null)
        super().__init__(self.__query,
                         self.__task,
                         self.__fun,
                         worker_args="worker_args",
                         num_workers=process_count)

    def scrape(self, query, count=50, quality=False, progressbar=False):
        self.__urls = set()
        if self.__process_count > 1:
            print("Gearing Up Quality Setting")
            quality = True
        self.__query.value = query.encode("utf-8")
        self.__task.value = True
        if quality:
            self.__fun.value = b"high_res"
        else:
            self.__fun.value = b"low_res"
        time.sleep(3)
        self.__fun.value = self.__null
        self.__progress_tracker(count, progressbar)
        self.__task.value = False
        self._flush_stream()
        return ScrapedResponse(query,
                               count,
                               len(self.__urls),
                               quality,
                               urls=list(self.__urls))

    def __progress_tracker(self, count, progressbar):
        output = self._output_stream()
        if progressbar:
            pbar = tqdm(total=count)
            pbar.set_description(f"Querying ({self.__query.value.decode()})")
            while len(self.__urls) < count:
                try:
                    if not output.empty():
                        url = output.get()
                        self.__urls.add(url)
                        pbar.update(1)
                except Exception as e:
                    print(e)
            pbar.close()
        else:
            while len(self.__urls) < count:
                try:
                    if not output.empty():
                        url = output.get()
                        self.__urls.add(url)
                except Exception as e:
                    print(e)

    def close(self):
        self._stop_workers()

    def __del__(self):
        return super().__del__()


if __name__ == "__main__":
    sc = Scraper(process_count=12)
    for query in ["Naruto", "Gintama"]:
        sc.scrape(query, progressbar=True).write().download(thread_count=8)

    sc.close()
