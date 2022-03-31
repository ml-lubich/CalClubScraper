# CalClubScraper
Scrapes all the emails of UC Berkeley's (Cal) student organizations (clubs). Outputs a .csv of the clubs and emails like so:

![screenshots/demo.png](.csv output)

Powered by Selenium and BeautifulSoup4.

---
## Runtime Enviornment
CalClubScraper runs using `pip` packages. It also requries you to download a `Chromedriver`. You also would need Python 3.6+

---
## Installation Steps 
1. If you have not already, install [Python 3.6+`](https://www.python.org/downloads/)
2. Install all `pip` required packages by `pip install requirements.txt`
3. Install the latest version of `chromedriver`: https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)

---
## Execute
To run the scraper, run `python3 src/webscraper_email.py` from the root directory.

---
## Sources
https://www.crummy.com/software/BeautifulSoup/bs4/doc/ BeautifulSoup4 documentation
https://selenium-python.readthedocs.io/ Selenium documentation
https://callink.berkeley.edu/ The website the program scrapes
