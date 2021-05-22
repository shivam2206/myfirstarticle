from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey

from myfirstarticle.database import db

__all__ = ['Article', 'ArticleView']


class Article(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    short_description = Column(String(300), nullable=False)
    long_description = Column(Text, nullable=False)
    published = Column(Boolean, default=False)
    created_on = Column(DateTime, default=datetime.utcnow)
    modified_on = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    author_id = Column(Integer, ForeignKey('author.id', ondelete='CASCADE'))
    views = Column(Integer, default=0)

    def __repr__(self):
        return f'<Article id={self.id} title={self.title}>'

    class Meta:
        allow_updates = ['title', 'short_description', 'long_description', 'published']


class ArticleView(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_on = Column(DateTime, default=datetime.utcnow)
    article_id = Column(Integer, ForeignKey('article.id', ondelete='CASCADE'))

    # TODO: Add more fields for better insights like location
