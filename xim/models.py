from app import app, db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from utils import get_hashed_password
from enum import Enum


def gen_uuid():
    return str(uuid.uuid4().hex)


class User(db.Model):
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
    id = db.Column(db.String(255), primary_key=True,
                   default=str(uuid.uuid4()))

    name = db.Column(db.String(255))
    url = db.Column(db.String(255))

    user_id = db.Column(db.String(255), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Alias: {self.id}>'

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class SearchableWebsite(Enum):
    GOOGLE = 'Google'
    WIKIPEDIA = 'Wikipedia'
    YOUTUBE = 'Youtube'
    AMAZON = 'Amazon'


class Shortcut(db.Model):
    id = db.Column(db.String(255), primary_key=True,
                   default=str(uuid.uuid4()))

    prefix = db.Column(db.String(255))
    website = db.Column(db.Enum(SearchableWebsite))

    user_id = db.Column(db.String(255), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Shortcut: {self.id}>'

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
