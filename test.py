from gi_scraper import Scraper

if __name__ == "__main__":

    queries = ["Naruto", "Gintoki", "Luffy", "Goku"]

    sc1 = Scraper()
    quality = "low"
    for query in queries:
        sc1.scrape(query, count=120,
                   progressbar=True).write(
                       path=f"./{quality}_quality",
                       filename=f"{query}_{quality}").download(
                           path=f"./{quality}_quality/{query}",
                           thread_count=12)
    sc1.close()

    quality = "high"

    sc2 = Scraper(process_count=4)
    for query in queries:
        sc2.scrape(query, count=120,
                   progressbar=True).write(
                       path=f"./{quality}_quality",
                       filename=f"{query}_{quality}").download(
                           path=f"./{quality}_quality/{query}",
                           thread_count=12)

    sc2.close()
