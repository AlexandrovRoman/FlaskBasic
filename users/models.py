import datetime
from flask_login import UserMixin
from app import db, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import base_new

roles_relationship = db.Table('roles_relationship',
                              db.Column('user_id', db.Integer, db.ForeignKey('users_list.id')),
                              db.Column('role_id', db.Integer, db.ForeignKey('roles_list.role_id')))


class User(db.Model, UserMixin):
    __tablename__ = 'users_list'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=True)
    surname = db.Column(db.String(80), nullable=True)
    fathername = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(40),
                      index=True, unique=True, nullable=True)
    hashed_password = db.Column(db.String, nullable=True)
    birth_date = db.Column(db.Date)
    age = db.Column(db.Integer)
    sex = db.Column(db.String(7), nullable=True)  # М/Ж
    grate = db.Column(db.String, default='Новичок')
    education = db.Column(db.String, default='Отсутствует')
    foreign_languges = db.Column(db.String, default='Отсутствует')
    start_place = db.Column(db.String)
    nationality = db.Column(db.String)
    marriage = db.Column(db.String(20))
    about_myself = db.Column(db.String, default='Отсутствует')
    organization_foreign_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=True)
    users = db.relationship('User', backref=db.backref('users_list', remote_side=[id]))
    personnel_id = db.Column(db.Integer, db.ForeignKey('users_list.id'))
    personnel = db.relationship("User", remote_side=[id])
    roles = db.relationship('Role', secondary=roles_relationship, backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    @property
    def get_profile_info(self):
        return {'Surname': self.surname, 'Name': self.name, 'Middle_name': self.fathername,
                'Gender': self.sex, 'Age': self.age, 'Grade': self.grate,
                'Education': self.education, 'Marital_status': self.marriage,
                'Knowledge_of_foreign_language': self.foreign_languges, 'Email': self.email,
                'About_myself': self.about_myself}

    def get_organizations(self):  # Наименование, Рабочие, Вакансии, id организации
        return [('Хлебобулочный комбинат', 0, 0, 1),
                ('ПФР пром. района', 1000, 500, 2),
                ('Автосервис Михаил-авто', 666, 69, 3)]

    def get_organization(self, org_id):  # todo Поменять заглушки на что-то рабочее
        if org_id is None:
            return None
        if org_id not in ['1', '2', '3']:  # Если пользователь не состоит в этой организации
            return None
        # Вернуть в зависимость от org_id
        return 1, 'ИП', 'Автосервис Михаил-авто', 'Ноябрь 2018', 'Тех. обслуживание; проверка авто перед покупкой; ремонтнык работы любой сложности.', 'Путь к картинке'

    def get_organization_department(self, org_id):  # todo Поменять заглушки на что-то рабочее
        if org_id is None:
            return None
        if org_id not in ['1', '2', '3']:  # Если пользователь не состоит в этой организации
            return None
        # Вернуть в зависимость от org_id
        return {
            'desc': (1, 'Автосервис Михаил-авто'),
            'personnel': [
                ('Васильев Оливер Юхимович', 25000, -1),  # ФИО, Зарплата, user_id
                ('Мамонтов Данила Михайлович', 26000, -1),
            ],
            'workers': [
                ('Федункив Сава Богданович', 'Управляющий', 30000, -1),  # ФИО, Должность, Зарплата, user_id
                ('Бирюков Мирослав Васильевич', 'Главный механик', 35000, -1),
            ],
            'required_workers': [
                ('Механик', 30000),  # Должность, Зарплата
            ],
        }

    def get_organization_list(self):  # todo Поменять заглушки на что-то рабочее
        return [
            (1, 'ИП', 'Автосервис Михаил-авто', 'Ноябрь 2018', 'Тех. обслуживание; проверка авто перед покупкой; ремонтнык работы любой сложности.', 'Путь к картинке')
        ]

    @staticmethod
    def get_logged(login, password):
        user = session.query(User).filter(User.email == login).first()
        if user and user.check_password(password):
            return user
        return None

    @staticmethod
    def get(user_id):
        return session.query(User).filter(User.id == user_id).first()

    @staticmethod
    def new(surname, name, fathername, birth_year, birth_month, birth_day,
            age, email, password, sex, marriage, org_id, roles='user'):
        kwargs = {"surname": surname, "name": name, "fathername": fathername,
                  "birth_date": datetime.date(birth_year, birth_month, birth_day),
                  "age": age, "email": email, "hashed_password": generate_password_hash(password),
                  "sex": sex, "marriage": marriage, "organization_foreign_id": org_id}
        special_commands = (f"cls.add_roles(obj, '{roles}')",)
        base_new(User, special_commands, **kwargs)

    @staticmethod
    def add_roles(user, role_names):
        for role_name in role_names.split():
            role = Role.query.filter_by(role_name=role_name).first()
            local_session_role = session.merge(role)
            user.roles.append(local_session_role)
        session.commit()


class Role(db.Model):
    __tablename__ = 'roles_list'

    role_id = db.Column(db.Integer,
                        primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(20), unique=True)
    description = db.Column(db.String(200))

    @staticmethod
    def new(name, description):
        kwargs = {"role_name": name, "description": description}
        base_new(Role, **kwargs)

    def __repr__(self):
        return '<Role {}, Возможности:{}>'.format(self.role_name, self.description)


# ЭТО ЗАГЛУШКА НЕ УДАЛЯТЬ
class Model1(db.Model):
    __tablename__ = 'model1'
    id = db.Column(db.Integer,
                   primary_key=True, autoincrement=True)
