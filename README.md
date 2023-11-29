# Google-Image-Scraper

## About

This module is based on web-scraping technology and uses Google Images to provide a Streamable Image API.

#### Supported Systems

- **Windows**

### Supported Browsers

- **Chrome**

## How to Use?

```python
# import Scraper class
from gi_scraper import Scraper

# The object creation has an overhead time
# The same object can be reused to fire multiple queries

sc = Scraper(headless=False)

for query, count in {"Naruto": 20, "Gintoki": 50, "Loki": 500}.items():
    print("Querying...", query)

    # scrape method returns a stream object
    stream = sc.scrape(query, count)

    # stream.get method yields Response object with following attributes
    # - query (str): The query associated with the response.
    # - name (str): The name attribute of the response.
    # - src_name (str): The source name attribute of the response.
    # - src_page (str): The source page attribute of the response.
    # - thumbnail (str): The thumbnail attribute of the response.
    # - image (str): The image attribute of the response.
    # - width (int): The width attribute of the response.
    # - height (int): The height attribute of the response.

    for response in stream.get():
        # response.to_dict returns python representable dictionary
        print(response.image, response.to_dict())

# call this to terminate scraping (auto-called by destructor)
sc.terminate()
```
