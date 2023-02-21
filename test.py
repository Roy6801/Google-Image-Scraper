# import Scraper class
from gi_scraper import Scraper

# The object creation has an overhead time
# The same object can be reused to fire multiple queries

sc = Scraper(workers=4, headless=False)

stream = sc.get_stream()

for query, count in {"Naruto": 50, "Gintoki": 50}.items():

    # 'get_stream' method returns a generator 'stream'
    # The module expects 'stream' to be called immediately
    # after a query is fired and doesn't allow
    # chaining queries directly.

    sc.scrape(query, count, timeout=5)

    # A Response object is returned from the stream
    # It that the following attributes:
    # name - Image Name,
    # position - Image Index in Google Images,
    # sourceName - Source Website Name,
    # sourcePage - Source WebPage,
    # thumbnail - Image Thumbnail,
    # url - Image URL

    for response in stream():
        # call 'to_dict' method for a python dictionary representation
        print(response.to_dict())
