from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from myfirstarticle.database import db

__all__ = ['Author']


class Author(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    verified = Column(Boolean, default=False)
    active = Column(Boolean, default=False)
    created_on = Column(DateTime, default=datetime.utcnow)
    articles = relationship('Article', backref='author')
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('Can\'t read password')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Author id={self.id} name={self.name}>'

    class Meta:
        allow_updates = ['name', 'active', 'password', 'verified']
