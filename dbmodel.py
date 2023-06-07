from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError, NoResultFound
db = SQLAlchemy()


class ArticleModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=False, nullable=False)
    link = db.Column(db.String, unique=True, nullable=False)
    domain = db.Column(db.String, unique=False, nullable=False)
    subdomain = db.Column(db.String, unique=False, nullable=True)
    time_stamp = db.Column(db.DateTime, unique=False, nullable=False)


class ArticleManager:
    def __init__(self, articles):
        self.articles = articles

    def create_article(self):
        for article in self.articles:
            link = article["link"]
            try:
                db.session.execute(db.select(ArticleModel).filter_by(link=link)).scalar_one()
            except NoResultFound:
                listing = ArticleModel(
                    title=article['title'],
                    link=article['link'],
                    domain=article['domain'],
                    subdomain=article['subdomain'],
                    time_stamp=article['time_published']
                )

                db.session.add(listing)
        db.session.commit()
