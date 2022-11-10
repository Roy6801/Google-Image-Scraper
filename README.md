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

</br>

```python
# import Scraper class
from gi_scraper import Scraper

# important since the library implements multiprocessing
if __name__ == "__main__":

    # creating Scraper object
    scraper = Scraper(process_count=4)

    for query in ["Naruto", "Gintoki", "Luffy", "Goku"]:
        
        # use scrape method to fire queries - returns ScrapedResponse object
        scraped_response = scraper.scrape(query, count, quality, progressbar, timeout)

        # default values
        # process_count=1
        # count=50
        # quality=False (works only for process_count=1)
        # progressbar=True
        # timeout=10 (in seconds)

        # setting process_count > 1 will change quality to True for every call to scrape method


        # dealing with ScrapedResponse object
        # write and download methods can be chained
        # writes to a json file
        # downloads .jpg images
        scraped_response.write(path="./", filename="query").download(path="./", thread_count=1)


        # get returns a dictionary with metadata and list of scraped urls
        # can be chained only at the end of the chained methods (write and download)
        scraped_response.get()
    

    # call close method or (del scraper) once scraping is done
    # needed for avoiding program going into an infinite loop
    scraper.close()
```
