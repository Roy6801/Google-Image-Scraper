from setuptools import setup, find_packages
from pathlib import Path

current_dir = Path(__file__).parent

VERSION = "0.4.4"
DESCRIPTION = "Google Image Scraper."
LONG_DESCRIPTION = (current_dir / "README.md").read_text()

setup(
    name="gi_scraper",
    version=VERSION,
    author="Roy6801",
    author_email="<mondal6801@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["selenium", "webdriver-manager"],
    keywords=[
        "python",
        "selenium",
        "web scraping",
        "images",
        "google image scraper",
        "web scraper",
        "image scraping",
        "google images",
        "image scraper",
        "image API",
        "API",
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ],
)
