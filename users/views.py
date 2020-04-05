from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app import login_manager, session
from organization.models import Organization
from users.models import User, Course


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@login_required
def profile():
    user = current_user
    info = user.get_profile_info
    info['hasAttached'] = Organization.get_attached_to_personnel(user) is not None
    return render_template('users/profile.html', **info)


@login_required
def edit_profile():
    user = current_user
    if request.method == 'POST':
        for attr in request.form:
            setattr(current_user, attr, request.form[attr])

        session.merge(current_user)
        session.commit()

        return redirect(url_for('profile'))
    info = user.get_profile_info
    info['hasAttached'] = Organization.get_attached_to_personnel(user) is not None

    return render_template('users/edit_profile.html', **info)


def login():
    if request.method == 'POST':
        user = User.get_logged(request.form['username'], request.form['password'])
        if user is not None:
            login_user(user)
            return redirect('/')

    return render_template('users/sign_in.html')


@login_required
def logout():
    logout_user()
    return redirect('/')


@login_required
def personnel():
    org = Organization.get_attached_to_personnel(current_user)
    if org is None:
        return 'Не привязан ни к одной'
    organization_info = {
        'org': org,
        'workers': org.get_workers(),
        'required_workers': org.get_required_workers(),
    }

    return render_template('users/personnel.html', **organization_info, len=len)


def education():
    return render_template("users/education.html", courses=Course.get_courses())


@login_required
def notification():
    user = current_user
    info = user.get_profile_info
    info['hasAttached'] = Organization.get_attached_to_personnel(user) is not None

    return render_template('users/notifications.html', **info)


def registration():
    return render_template("users/registration.html")


@login_required
def t2():
    user_id = request.args['user_id']
    user = current_user
    if False:  # TODO: Если не обладает правами кадровика над человеком с user_id
        return 'Нет доступа к форме этого пользователя'
    target = User.get(user_id)

    # TODO: Create html templates
    if target is None:
        return 'Нет пользователя'
    if not target.t2_rel:  # Если не обладает формой T2
        return 'Нет формы T2'

    return render_template("users/T2.html", form=target.t2_rel[0])
