# Google-Image-Scraper

About
---------------------------------------------------------------------
Image scraping is required many a times for web-based and machine
learning projects.
This module will help in fetching or downloading images from google.
---------------------------------------------------------------------


How to Use?
---------------------------------------------------------------------
This module is to be used along with chromedriver.
Download correct version of chromedriver from here:-

Link - https://chromedriver.chromium.org/downloads

Place the chromedriver.exe in the same directory as the scraper.py
and progressbar.py file.
The scraper module has class Scraper within which is defined the
fetch function that will return a dictionary of image urls of the
query passed number from 0 to [(Count - 1) entered].

Import Scraper class:-

from scraper import Scraper

urlDict = Scraper().fetch(self, query, count=50, tCount=1,
quality=True, downloadImages=False, saveList=False)

query   :   Images that you are looking for.
count   :   Number of Images required. (Max. : 120 for quality
            = True, Max. : 300 for quality = False)
tCount  :   Number of threads (Max. : 4)
quality :   When True, will return higher image quality urls.
downloadImages  :   Set this True to download the images to a
                    folder.
saveList    :   Set this True to save list of urls to a folder.

urlDict will contain the dictionary of image urls that can be used
anywhere in the program.
---------------------------------------------------------------------