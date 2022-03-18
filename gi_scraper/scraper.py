from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from multiprocessing import Process, Queue
from threading import Thread
from driver_manager import Manager
from utils import *
from urllib import parse
from tqdm import tqdm
import time


def scrape(query,
           count=50,
           pCount=1,
           tCount=1,
           quality=True,
           downloadImages=False,
           saveList=False,
           defaultDir=False,
           dirPath="",
           driverPath=""):
    query = query.strip()

    count = abs(int(count))
    pCount = abs(int(pCount))
    tCount = abs(int(tCount))

    url = "https://www.google.com/search?{}&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjR5qK3rcbxAhXYF3IKHYiBDf8Q_AUoAXoECAEQAw&biw=1291&bih=590"
    url = url.format(parse.urlencode({'q': query}))

    if driverPath == "":
        driverPath = Manager().chromeDriver()
    driverPath = driverPath.replace("/", "\\")

    images = Queue(maxsize=count)

    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--headless")
    options.add_argument('--log-level=3')

    if pCount > 8:
        pCount = 8
        print("PROCESS COUNT SET : ", pCount, ", LIMITING TO 8")
    else:
        print("PROCESS COUNT SET : ", pCount)

    if tCount > 8:
        tCount = 8
        print("THREAD COUNT SET : ", tCount, ", LIMITING TO 8")
    else:
        print("THREAD COUNT SET : ", tCount)

    if quality:
        fetch = fetch1
        if count > 150:
            print("QUALITY SET : TRUE, GIVEN COUNT :", count,
                  ", LIMITING TO : 150")
            count = 150
    else:
        fetch = fetch2
        if count > 300:
            print("QUALITY SET : FALSE, GIVEN COUNT :", count,
                  ", LIMITING TO : 300")
            count = 300

    processes = []

    for pid in range(pCount):
        prc = Process(target=fetch,
                      args=(url, images, driverPath, options, pid))
        processes.append(prc)
        prc.start()

    prevSize = -1

    pbar = tqdm(total=count)

    while not images.full():
        currSize = images.qsize()
        pbar.update(currSize - prevSize)
        prevSize = currSize

    pbar.close()

    if downloadImages or saveList:

        dirName = createDir(query, defaultDir, dirPath)

        if download_images:
            threads = []

            imagesURL = []

            while not images.empty():
                imagesURL.append(images.get())

            imagesURL = list(set(imagesURL))

            for tid in range(tCount):
                thr = Thread(target=download_images,
                             args=(query, imagesURL, dirName, tCount, tid))
                threads.append(thr)
                thr.start()

            for thr in threads:
                thr.join()

        if saveList:
            saveToList(images, dirName, query)

        urlDict = {k: v for k, v in enumerate(imagesURL)}

        return urlDict


def fetch1(url, images, driverPath, options, pid=0):
    driver = webdriver.Chrome(executable_path=driverPath,
                              chrome_options=options)
    driver.get(url)

    try:
        y = 0
        if pid == 0:
            cnt = 0
        else:
            cnt = 50 * pid

        while True:
            cnt += 1
            if images.full(): break
            driver.execute_script(f"window.scrollBy(0, {y});")
            element = driver.find_element(By.ID, "islmp")
            anchors = element.find_elements(
                By.CSS_SELECTOR,
                f"#islrg > div.islrc > div:nth-child({cnt}) > a.wXeWr.islib.nfEiy"
            )
            for anchor in anchors:
                ActionChains(driver).click(anchor).perform()
                time.sleep(1.0)
                img = anchor.find_element(
                    By.XPATH,
                    '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img'
                )
                if images.full(): break
                else:
                    src = img.get_attribute("src")
                    if src is None: continue
                    src = str(src)
                    if src.startswith("data:image/") or src.startswith(
                            "https://encrypted"):
                        continue
                    images.put(src)
                driver.back()
            y += 1000
    except Exception as e:
        pass


def fetch2(url, images, driverPath, options, pid=0):
    driver = webdriver.Chrome(executable_path=driverPath,
                              chrome_options=options)
    driver.get(url)

    try:
        y = pid * 1000

        while True:
            if images.full(): break
            driver.execute_script(f"window.scrollBy(0, {y});")
            imgs = driver.find_elements(By.CLASS_NAME, "rg_i")
            for img in imgs:
                src = img.get_attribute("src")
                if images.full(): break
                else:
                    if src is None: continue
                    src = str(src)
                    images.put(src)
            y += 10
    except Exception as e:
        pass
