from flask import jsonify
from flask_restful import reqparse
from app.api_utils import get_or_abort
from app.BaseAPI import BasicResource
from users.models import User
from .views import Registration
# import re


def get_or_abort_user(user_id):
    return get_or_abort(user_id, User)


class UserResource(BasicResource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True)
    parser.add_argument('surname', required=True)
    parser.add_argument('fathername', required=True)
    parser.add_argument('email', required=True)
    parser.add_argument('password', required=True)

    def get(self, user_id):
        self.set_authorized_user()
        if not self.authorized_user:
            return self.basic_error('Login before using API')
        user = get_or_abort_user(user_id)

        return jsonify({'user': user.to_dict(
            only=('id', 'name', 'surname', 'fathername', 'birth_date'))})

    def delete(self, user_id):
        self.set_authorized_user()
        if not self.authorized_user:
            return self.basic_error('Login before using API')

        if user_id != self.authorized_user.id:
            return self.basic_error('delete is not allowed to this user')

        user = get_or_abort_user(user_id)
        user.delete()
        return jsonify({'deleting': 'OK'})

    def post(self):
        self.set_authorized_user()
        if not self.authorized_user:
            return self.basic_error('Login before using API')

        # При использовании этого метода появляется smtplib.SMTPAuthenticationError: (501,
        # b'5.5.2 Cannot Decode response h12sm4255952lji.25 - gsmtp'), остальное работает
        args = self.parser.parse_args()
        if User.get_by(email=args['email']):
            return self.basic_error('email already taken')

        if any(map(str.isdigit, args['name'] + args['surname'] + args['fathername'])):
            return self.basic_error('invalid name, surname or fathername')

        # if not re.search(r".+@.+\..+", args["email"]):  # .+ - любое количество, любых символов, \ - экранирование символа
        #     return self.basic_error('invalid email')

        if '@' not in args['email'] or '.' not in args['email']:
             return self.basic_error('invalid email')

        user = User(
            name=args['name'],
            surname=args['surname'],
            fathername=args['fathername'],
            email=args['email'],
            password=args['password']
        )
        user.save(add=True)
        Registration.send_email(user)

        return jsonify({'adding': 'OK'})
