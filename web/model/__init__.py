from .core import db

import uuid
from enum import Enum

from sqlalchemy.dialects.postgresql import UUID
from flask_login import UserMixin


def gen_uuid():
    return str(uuid.uuid4().hex)


class User(UserMixin, db.Model):
    id = db.Column(db.String(), primary_key=True, default=gen_uuid)

    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    aliases = db.relationship('Alias', backref='user')
    shortcuts = db.relationship('Shortcut', backref='user')

    def __repr__(self):
        return f'<User: {self.id}>'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Alias(db.Model):
    id = db.Column(db.String(), primary_key=True, default=gen_uuid)

    name = db.Column(db.String(255))
    url = db.Column(db.String(255))

    user_id = db.Column(db.String(255), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Alias: {self.id}>'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class SearchableWebsite(str, Enum):
    GOOGLE = 'GOOGLE'
    WIKIPEDIA = 'WIKIPEDIA'
    YOUTUBE = 'YOUTUBE'
    AMAZON = 'AMAZON'


class Shortcut(db.Model):
    id = db.Column(db.String(), primary_key=True, default=gen_uuid)

    prefix = db.Column(db.String(255))
    website = db.Column(db.Enum(SearchableWebsite))

    user_id = db.Column(db.String(255), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Shortcut: {self.id}>'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
