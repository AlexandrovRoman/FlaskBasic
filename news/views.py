from flask import render_template
from news.models import News, Courses


def index():
    news = [(i, *j) for i, j in enumerate(News.get_news())]
    courses = Courses.get_courses()
    return render_template('news/news.html', news=news, courses=enumerate(courses))
