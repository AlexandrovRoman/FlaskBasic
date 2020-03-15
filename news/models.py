from app import db
import datetime
from app.models import base_new


class News(db.Model):
    __tablename__ = 'news_table'

    id = db.Column(db.Integer,
                   primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), nullable=True)
    description = db.Column(db.String, nullable=True)
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    tags = db.Column(db.String, nullable=True)  # Тэги новости через запятую
    link = db.Column(db.String, default='#')

    def __repr__(self):
        return '<News {}>'.format(self.title)

    @classmethod
    def get_news(cls):
        news = [(obj.title, obj.description, obj.link) for obj in cls.query.all()]
        return news

    @classmethod
    def new(cls, title, description, link='#'):
        kwargs = {"title": title, "description": description, "link": link}
        base_new(cls, **kwargs)


class Courses(db.Model):
    __tablename__ = 'courses_table'

    id = db.Column(db.Integer,
                   primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), nullable=True)
    description = db.Column(db.String, nullable=True)
    image_link = db.Column(db.String, nullable=True)

    def __repr__(self):
        return '<News {}>'.format(self.title)

    @classmethod
    def get_courses(cls):
        courses = [(obj.title, obj.description, obj.image_link) for obj in cls.query.all()]
        return courses

    @classmethod
    def new(cls, title, description, image_link):
        kwargs = {"title": title, "description": description, "image_link": image_link}
        base_new(cls, **kwargs)
