# Google-Image-Scraper

## About

Image scraping is required many a times for web-based and machine
learning projects.
This module will help in fetching or downloading images from google.

#### Supported Systems

- **Windows**

### Supported Browsers

- **Chrome**

## How to Use?

This module is to be used along with **chromedriver**.
Download correct version of chromedriver from here:-

## Link - https://chromedriver.chromium.org/downloads

```python
from gi_scraper import scrape

urlDict = scrape(query="Search Query", count=50, tCount=1, quality=True, downloadImages=False, saveList=False, defaultDir=False, dirPath="", driverPath="/path/to/chromedriver.exe")
```

| Parameter      | Description                                                                                                                                                                                                                     | Default                   |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------- |
| driverPath     | Scraper(driverPath="Path to chromedriver.exe")                                                                                                                                                                                  | Current Working Directory |
| query          | Images that you are looking for.                                                                                                                                                                                                | -                         |
| count          | Number of Images required. (Max. : 150 for quality = True, Max. : 300 for quality = False).                                                                                                                                     | 50                        |
| tCount         | Number of threads (Max. : 8).                                                                                                                                                                                                   | 1                         |
| quality        | True: fetches only high image quality urls or images.                                                                                                                                                                           | True                      |
| downloadImages | True: download the images to a folder.                                                                                                                                                                                          | False                     |
| saveList       | True: save list of urls to a folder.                                                                                                                                                                                            | False                     |
| defaultDir     | True: save files to a folder created at current working directory. False: prompts for directory selection.                                                                                                                      | False                     |
| dirPath        | Set path to your default download/save directory. This will avoid prompting for path during download. This setting also overrides defaultDir in which download path is current working directory by setting it to entered path. | Not Set                   |

urlDict will contain the dictionary of image urls that can be used anywhere in the program.
