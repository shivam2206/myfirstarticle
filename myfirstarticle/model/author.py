from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from myfirstarticle.database import db


class Author(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    verified = Column(Boolean, default=False)
    active = Column(Boolean, default=False)
    created_on = Column(DateTime, default=datetime.utcnow)
    articles = relationship('Article', backref='author')

    def __repr__(self):
        return f'<Author id={self.id} name={self.name}>'
