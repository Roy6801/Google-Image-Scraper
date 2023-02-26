from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from threading import Thread
from queue import Queue
from urllib import parse
import time
from .response import Response


class Scraper:

    def __init__(self, workers=1, headless=True):
        self.__workers = workers
        self.__worker_threads = []
        self.__headless = headless
        self.__drivers = []
        self._driver_init()
        self.__images = set()
        self.__imqueue = Queue()
        self.__interrupt = False
        self.__cleanup = lambda x: int(float(x.replace("px;", "")))
        self._setup()

    def _setup(self):

        thread = Thread(target=self._driver_init)
        thread.start()
        thread.join()

        driver_threads = []

        for _ in range(self.__workers):
            thread = Thread(target=self._spawn_driver)
            driver_threads.append(thread)
            thread.start()

        for thread in driver_threads:
            thread.join()

    def _driver_init(self):
        self.__driver_path = ChromeDriverManager(path="./").install()
        self.__options = webdriver.ChromeOptions()
        self.__options.add_argument("ignore-certificate-errors")
        self.__options.add_argument("incognito")
        if self.__headless:
            self.__options.add_argument("headless")
        self.__options.add_argument("log-level=3")
        self.__options.add_argument("disable-gpu")
        self.__options.add_experimental_option('excludeSwitches',
                                               ['enable-logging'])

    def _spawn_driver(self):
        driver = webdriver.Chrome(service=Service(self.__driver_path),
                                  options=self.__options)

        driver.get("https://www.google.com/")
        self.__drivers.append(driver)

    def _spawn_workers(self):
        self.__interrupt = False
        for i in range(self.__workers):
            thread = Thread(target=self._get_images,
                            args=(i + 1, self.__drivers[i]))
            self.__worker_threads.append(thread)
            thread.start()

    def _destroy_workers(self):
        self.__interrupt = True
        for thread in self.__worker_threads:
            thread.join()
        self.__worker_threads = []

    def _get_images(self, id, driver):
        url_frame = "https://www.google.com/search?{}&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjR5qK3rcbxAhXYF3IKHYiBDf8Q_AUoAXoECAEQAw&biw=1291&bih=590"
        url = url_frame.format(parse.urlencode({'q': self.__query}))
        driver.get(url)

        delay = 3  # seconds
        index = id

        while len(self.__images) < self.__count:
            try:
                if self.__interrupt:
                    break
                action = ActionChains(driver)
                wait = WebDriverWait(driver, delay)

                img = driver.find_element(
                    By.XPATH,
                    f'//*[@id="islrg"]/div[1]/div[{index}]/a[1]/div[1]/img')

                # Thumbnail
                img_thumb = img.get_attribute("src")

                # Image Title
                img_name = img.get_attribute("alt")

                action.click(img).perform()
                elements = wait.until(
                    EC.presence_of_all_elements_located(
                        (By.CLASS_NAME, "KAlRDb")))

                img_element = elements[-1]

                # Image URL
                img_url = img_element.get_attribute("src")
                img_dim = img_element.get_attribute("style")

                img_dim = img_dim.split(" ")

                img_width = self.__cleanup(img_dim[1])
                img_height = self.__cleanup(img_dim[3])

                # //*[@id="islrg"]/div[1]/div[1]/a[1]/div[1]/img
                # //*[@id="islrg"]/div[1]/div[51]/a[1]/div[1]/img

                src_element = driver.find_element(
                    By.XPATH,
                    '//*[@id="Sva75c"]/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div/div[1]/div[1]/div[1]/a/div/div[2]/div/div'
                )

                # Source Website Name
                img_src_name = src_element.text

                src_url_element = driver.find_element(
                    By.XPATH,
                    '//*[@id="Sva75c"]/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div/div[1]/div[4]/div[1]/a[1]'
                )

                # Source Website URL

                img_src_page = src_url_element.get_attribute("href")

                response = Response(name=img_name,
                                    position=index,
                                    sourceName=img_src_name,
                                    sourcePage=img_src_page,
                                    thumbnail=img_thumb,
                                    url=img_url,
                                    width=img_width,
                                    height=img_height)
                self.__imqueue.put(response)
                index += self.__workers

            except Exception as e:
                if self.__interrupt:
                    break
                index += self.__workers

    def _stream(self):
        while len(self.__images) < self.__count:
            if not self.__imqueue.empty():
                self.__start_time = int(time.time())
                image_object = self.__imqueue.get()
                if image_object.url not in self.__images:
                    self.__images.add(image_object.url)
                    yield image_object
            else:
                if int(time.time()) - self.__start_time >= self.__timeout:
                    print("Timed out")
                    break

        self._destroy_workers()
        self._flush_stream()

    def _flush_stream(self):
        while not self.__imqueue.empty():
            self.__imqueue.get()
        self.__images = set()

    def scrape(self, query, count, timeout=10):
        self.__query = query
        self.__count = count
        self.__timeout = timeout
        self.__start_time = int(time.time())
        self._spawn_workers()

        return self._stream
