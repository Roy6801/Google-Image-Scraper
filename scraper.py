from selenium import webdriver
from selenium.webdriver import ActionChains
from threading import Thread
from progressbar import ProgressBar
from tkinter.filedialog import askdirectory
from urllib import parse, request
import time
from tkinter import Tk
import os

class Scraper:
    def __init__(self):
        self.images = dict()
        self.ctr = 0
        self.url = "https://www.google.com/search?{}&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjR5qK3rcbxAhXYF3IKHYiBDf8Q_AUoAXoECAEQAw&biw=1291&bih=590"        
    
    def fetch(self, query, count=50, tCount=1, quality=True, downloadImages=False, saveList=False):
        
        def createDir():
            root = Tk()
            root.withdraw()
            root.attributes("-topmost", True)
            directory = askdirectory(parent=root)
            
            if directory is not None:
                if len(directory) == 0:
                    print("No Directory Selected... Creating Default Directory!")
                    directory = os.getcwd() + "\\GIS Downloads\\" + query
                else:
                    directory = directory + "\\GIS Downloads\\" + query
                    directory.replace("/", "\\")
            else:
                print("No Directory Selected... Creating Default Directory!")
                directory = os.getcwd() + "\\GIS Downloads\\" + query
            
            os.makedirs(directory, exist_ok=True)
            print("Saving to... ", directory)
            return directory
        
        thr = []
        query = query.strip()

        if tCount > 4:
            tCount = 4
            print("THREAD COUNT SET : ", tCount, ", LIMITING TO 4")
        else:
            print("THREAD COUNT SET : ", tCount)

        if quality:
            fetch = self.sub_fetch1
            if count > 120:
                print("QUALITY SET : TRUE, GIVEN COUNT :", count ,", LIMITING TO : 120")
                count = 120
        else:
            fetch = self.sub_fetch2
            if count > 300:
                print("QUALITY SET : FALSE, GIVEN COUNT :", count ,", LIMITING TO : 300")
                count = 300
        
        self.pb = ProgressBar(count, "Getting Images")
        
        for i in range(tCount):
            t = Thread(target=fetch, args=(query, count, i))
            thr.append(t)
            t.start()
        
        for t in thr:
            t.join()
        
        del self.pb
        
        if downloadImages:
            self.completed = 0
            pCount = tCount
            dirName = createDir()

            pcr = []
            self.downloader = ProgressBar(len(self.images), "Downloading Images")
            for i in range(pCount):
                p = Thread(target=self.download_images, args=(query, dirName, pCount, i))
                pcr.append(p)
                p.start()
            
            for p in pcr:
                p.join()
            
            del self.downloader
        
        if saveList:
            dirName = createDir()
            self.saveToList(dirName)
        
        return self.images
    
    def sub_fetch1(self, query, count=100, tid=0):
        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")
        options.add_argument("--headless")
        options.add_argument('--log-level=3')
        driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=options)
        url = self.url.format(parse.urlencode({'q': query}))
        driver.get(url)
        try:
            y = 0
            if tid == 0:
                cnt = 0
            else:
                cnt = 50 * tid

            while True:
                cnt += 1
                if len(self.images) >= count:break
                driver.execute_script("window.scrollBy(0, {});".format(y))
                element = driver.find_element_by_id("islmp")
                anchors = element.find_elements_by_css_selector("#islrg > div.islrc > div:nth-child({}) > a.wXeWr.islib.nfEiy".format(cnt))
                for anchor in anchors:
                    ActionChains(driver).click(anchor).perform()
                    time.sleep(1.0)
                    img = anchor.find_element_by_xpath('//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img')
                    if len(self.images) >= count:break
                    else:
                        src = img.get_attribute("src")
                        if src is None:continue
                        src = str(src)
                        if src.startswith("data:image/") or src.startswith("https://encrypted"):continue
                        if src not in self.images.values():
                            self.images[self.ctr] = src
                            self.ctr += 1
                    driver.back()
                y += 1000
                self.pb.ProgressBar(self.ctr)
        except Exception as e:
            pass
    
    def sub_fetch2(self, query, count=100, tid=0):
        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")
        options.add_argument("--headless")
        options.add_argument('--log-level=3')
        driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=options)
        url = self.url.format(parse.urlencode({'q': query}))
        driver.get(url)

        try:
            y = tid * 1000

            while True:
                if len(self.images) >= count:break
                driver.execute_script("window.scrollBy(0, {});".format(y))
                imgs = driver.find_elements_by_class_name("rg_i")
                for img in imgs:
                    src = img.get_attribute("src")
                    if len(self.images) >= count:break
                    else:
                        if src is None:continue
                        src = str(src)
                        if src not in self.images.values():
                            self.images[self.ctr] = src
                            self.ctr += 1
                y += 10
                self.pb.ProgressBar(self.ctr)
        except Exception as e:
            pass
    
    def download_images(self, query, dir, pCount=1, tid=0):
        totalTaskLength = len(self.images)
        taskLength = totalTaskLength//pCount
        chunkStart = tid * taskLength
        if tid == pCount - 1:
            chunkEnd = len(self.images)
        else:
            chunkEnd = chunkStart + taskLength
        
        for index in range(chunkStart, chunkEnd):
            img = self.images[index]
            file = dir + "\\" + query + "_" + str(tid) + "_" + str(index).rjust(3,'0') + ".jpg"
            try:
                request.urlretrieve(img, file)
                self.completed += 1
                self.downloader.ProgressBar(self.completed)
            except Exception as e:
                pass
    
    def saveToList(self, dirName):
        dirName = dirName + "\\urls.txt"
        try:
            os.remove(dirName)
        except:
            pass
        with open(dirName, "a") as fa:
            for index, link in self.images.items():
                fa.write(str(index) + " : " + link + "\n")
