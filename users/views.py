from typing import List, Tuple

from flask import render_template, request, make_response

current_users: List[Tuple[str, str]] = [
    ('aaa', '111'),
    ('ggg', '123'),
]


def hello():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for i, j in current_users:
            if i == username and j == password:
                return render_template('news.html')

        # return render_template('news.html')
    return render_template('profile.html')


def cookie_test():
    click_count = cook if (cook := request.cookies.get('click')) else '2'
    res = make_response(f"Your click count is {click_count}")
    res.set_cookie('click', str(int(click_count) + 1), max_age=1)

    return res


def index():
    return render_template('news.html')
