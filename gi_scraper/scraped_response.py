from threading import Thread
from urllib import request
from tqdm import tqdm
import json
import os


class ScrapedResponse:

    def __init__(self,
                 query=None,
                 count=0,
                 scraped_count=0,
                 quality=None,
                 urls=[]):
        self.__query = query
        self.__count = count
        self.__scraped_count = scraped_count
        self.__quality = quality
        self.__urls = urls
        self.__response = {
            "query": self.__query,
            "count": self.__count,
            "scraped_count": self.__scraped_count,
            "quality": self.__quality,
            "urls": self.__urls
        }

    def get(self):
        return self.__response

    def download(self, path=None, thread_count=1):
        if not path:
            path = self.__query
        os.makedirs(path, exist_ok=True)

        task_length = self.__scraped_count // thread_count
        opener = request.build_opener()
        opener.addheaders = [(
            'User-Agent',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'
        )]
        request.install_opener(opener)

        pbar = tqdm(total=self.__scraped_count)
        pbar.set_description(f"Downloading ({self.__query})")

        threads = []

        for tid in range(0, thread_count):
            chunk_start = tid * task_length
            chunk_end = chunk_start + task_length
            if tid == thread_count - 1:
                chunk_end = self.__scraped_count
            thread = Thread(target=self.__downloader,
                            args=(tid, path, chunk_start, chunk_end, request,
                                  pbar))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        pbar.close()

        return self

    def __downloader(self, tid, folderpath, chunk_start, chunk_end, request,
                     progressbar):
        for index in range(chunk_start, chunk_end):
            img = self.__urls[index]
            filename = f"{folderpath}\\{self.__query}_{str(tid)}_{str(index).rjust(3,'0')}.jpg"
            try:
                request.urlretrieve(img, filename)
                progressbar.update(1)
            except Exception as e:
                print(e)

    def write(self, path="./", filename=None):
        if not filename:
            filename = self.__query
        filepath = os.path.join(path, filename)
        os.makedirs(path, exist_ok=True)

        with open(f"{filepath}.json", "w") as fw:
            json.dump(self.__response, fw)
        return self
