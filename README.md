# Google-Image-Scraper

About
---
Image scraping is required many a times for web-based and machine
learning projects.
This module will help in fetching or downloading images from google.

How to Use?
---
This module is to be used along with chromedriver.
Download correct version of chromedriver from here:-

Link - https://chromedriver.chromium.org/downloads
---

Place the chromedriver.exe in the same directory as the scraper.py and progressbar.py file.
The scraper module has class Scraper within which is defined the
fetch function that will return a dictionary of image urls of the
query passed number from 0 to [(Count - 1) entered].

Import Scraper class:-

from scraper import Scraper

urlDict = Scraper().fetch(query="Search Query", count=50, tCount=1, quality=True, downloadImages=False, saveList=False, defaultDir=False, dirPath="")

or

urlDict = Scraper(driverPath="chromedriver.exe").fetch(query="Search Query", count=50, tCount=1, quality=True, downloadImages=False, saveList=False, defaultDir=False, dirPath="")

driverPath  :   Scraper() object by default looks for chromedriver.exe in current working
                directory. Using Scraper(driverPath="Path to chromedriver.exe") will
                allow using it from other directory.

query   :   Images that you are looking for. No Default.

count   :   Number of Images required. (Max. : 150 for quality
            = True, Max. : 300 for quality = False). Default : 50.

tCount  :   Number of threads (Max. : 8). Default : 1.

quality :   When True, will return higher image quality urls. Default : True.

downloadImages  :   Set this True to download the images to a
                    folder. Default : False.

saveList    :   Set this True to save list of urls to a folder. Default : False.

defaultDir	:	Set True to save files to a folder created at current working directory.
				Set False to get prompted for directory selection. Default : False.

dirPath     :   Set path to your default download/save directory. This will avoid prompting
                for path during download. This setting also overrides defaultDir in which download path is current working directory by setting it to entered path.
                 Default : Not Set.

urlDict will contain the dictionary of image urls that can be used anywhere in the program.
