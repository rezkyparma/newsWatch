import scrapper

# Address of publisher index page
DETIK_NEWS = "https://news.detik.com/indeks"
DETIK_SPORT = "https://sport.detik.com/indeks"
KOMPAS = "https://indeks.kompas.com/"

# List of URL for each parent domain
detik_list_url = [DETIK_NEWS, DETIK_SPORT]
kompas_list_url = [KOMPAS]

# Target articles scrapped for each URL
TARGET_ARTICLE = 35


detik = scrapper.DetikScrapper(detik_list_url, TARGET_ARTICLE, print=False).detik_crawler()
print(len(detik))

kompas = scrapper.KompasScrapper(kompas_list_url, TARGET_ARTICLE, print=False).kompas_crawler()
print(len(kompas))