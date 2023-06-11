from source import detik_list_url, kompas_list_url
from scrapper import DetikScrapper, KompasScrapper
from flask import Flask, render_template, request, redirect
from dbmodel import ArticleManager, db
from openai_call import ArticleEvaluate

# Initialize Flask
app = Flask(__name__)

# Initialize DB
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

openai = ArticleEvaluate("https://finance.detik.com/berita-ekonomi-bisnis/d-6765426/kemenkeu-hormati-permintaan-jusuf-hamka-tagih-utang-rp-800-m").get_info()

# Main function to scrap
detik = DetikScrapper(detik_list_url, 0, print=False).detik_crawler()
kompas = KompasScrapper(kompas_list_url, 1, print=False).kompas_crawler()

# Extending returned list to all article that will be passed into dbmodel method
all_article = []
lists_to_extend = [detik, kompas]  # Add more lists here as needed
for lst in lists_to_extend:
    all_article.extend(lst)

# Write basic article info to db
with app.app_context():
    ArticleManager(all_article).create_article()
    db.create_all()

print(openai)
print(f'Detik: {len(detik)}')
print(f'Kompas: {len(kompas)}')


if __name__ == "__main__":
    pass

