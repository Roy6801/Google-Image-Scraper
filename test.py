# import Scraper class
from gi_scraper import Scraper

# The object creation has an overhead time
# The same object can be reused to fire multiple queries

sc = Scraper(headless=False)

for query, count in {"Naruto": 200, "Gintoki": 300}.items():
    # scrape method returns a stream object
    stream = sc.scrape(query, count)
    i = 0

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
        if i == 20:
            sc.terminate_query()  # Terminate current query midway
            break
        # response.to_dict returns python representable dictionary
        print(response.width, "x", response.height, ":", response.image)
        i += 1

# call this to terminate scraping (auto-called by destructor)
sc.terminate()
