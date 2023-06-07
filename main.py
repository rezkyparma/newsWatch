import scrapper
from flask import Flask, render_template, request, redirect
from dbmodel import ArticleManager, db

# Address of publisher index page
DETIK_NEWS = "https://news.detik.com/indeks"
DETIK_SPORT = "https://sport.detik.com/indeks"
DETIK_EDU = "https://www.detik.com/edu/indeks"
DETIK_FINANCE = "https://finance.detik.com/indeks"
DETIK_HOT = "https://hot.detik.com/indeks"
DETIK_INET = "https://inet.detik.com/indeks"
DETIK_OTO = "https://oto.detik.com/indeks"
DETIK_TRAVEL = "https://travel.detik.com/indeks"  # Excluded due to different structure
DETIK_SEPAKBOLA = "https://sport.detik.com/sepakbola/indeks"
DETIK_FOOD = "https://food.detik.com/indeks"
DETIK_HEALTH = "https://health.detik.com/indeks"
DETIK_WOLIPOP = "https://wolipop.detik.com/indeks"
DETIK_JATIM = "https://www.detik.com/jatim/indeks"
DETIK_JATENG = "https://www.detik.com/jateng/indeks"
DETIK_JABAR = "https://www.detik.com/jabar/indeks"
DETIK_SULSEL = "https://www.detik.com/sulsel/indeks"
DETIK_SUMUT = "https://www.detik.com/sumut/indeks"
DETIK_BALI = "https://www.detik.com/bali/indeks"
DETIK_HIKMAH = "https://www.detik.com/hikmah/indeks"
DETIK_SUMBAGSEL = "https://www.detik.com/sumbagsel/indeks"
KOMPAS = "https://indeks.kompas.com/"
# List of URL for each parent domain
detik_list_url = [DETIK_NEWS, DETIK_SPORT, DETIK_EDU, DETIK_FINANCE, DETIK_HOT, DETIK_INET, DETIK_OTO,
                  DETIK_SEPAKBOLA, DETIK_FOOD, DETIK_HEALTH, DETIK_WOLIPOP, DETIK_JATIM, DETIK_JATENG, DETIK_JABAR,
                  DETIK_SULSEL, DETIK_SUMUT, DETIK_BALI, DETIK_HIKMAH, DETIK_SUMBAGSEL]
kompas_list_url = [KOMPAS]
# Target articles scrapped for each URL
TARGET_ARTICLE = 1

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

if __name__ == "__main__":
    pass

# Main function to scrap
detik = scrapper.DetikScrapper(detik_list_url, TARGET_ARTICLE, print=False).detik_crawler()
kompas = scrapper.KompasScrapper(kompas_list_url, TARGET_ARTICLE, print=False).kompas_crawler()

# Extending returned list to all article then it will be passed into dbmodel method
all_article = []
lists_to_extend = [detik, kompas]  # Add more lists here as needed

for lst in lists_to_extend:
    all_article.extend(lst)

with app.app_context():
    ArticleManager(all_article).create_article()
    db.create_all()

print(f'Detik: {len(detik)}')
print(f'Kompas: {len(kompas)}')
