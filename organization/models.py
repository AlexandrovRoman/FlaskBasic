from app import db
from datetime import datetime
from utils.models import ModelMixin
from sqlalchemy_serializer import SerializerMixin
from utils.api import create_jwt


class Organization(db.Model, ModelMixin, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=True)
    creation_date = db.Column(db.Date, default=datetime.now)
    personnels = db.relationship("User", backref='binded_org', lazy='select')
    vacancies = db.relationship("Vacancy", backref='organization')
    owner_id = db.Column(db.Integer)
    org_type = db.Column(db.String)
    org_desc = db.Column(db.String)
    api_token = db.Column(db.String)

    def __init__(self,
                 name=None,
                 owner_id=None,
                 org_type=None,
                 org_desc=None,
                 date=None):
        super().__init__(name=name, owner_id=owner_id, org_desc=org_desc, org_type=org_type, creation_date=date)
        self.refresh_token()

    def __repr__(self):
        return f'<Organization {self.name}>'

    @classmethod
    def get_by_id(cls, user, org_id: int):
        org = cls.get_by(id=org_id)
        return org if user.id == org.owner_id else None

    @classmethod
    def get_attached_to_user(cls, user):
        return cls.query.filter_by(owner_id=user.id).all()

    @classmethod
    def new(cls, name, owner_id, org_type, org_desc, date=None):
        date = date if date else datetime.now()
        super().new(name, owner_id, org_type, org_desc, date)

    def get_required_workers(self):
        return [vacancy for vacancy in self.vacancies if vacancy.worker_id is None]

    def get_workers(self):
        return [vacancy for vacancy in self.vacancies if vacancy.worker_id is not None]

    def refresh_token(self):
        self.api_token = create_jwt(self.name)


class Vacancy(db.Model, ModelMixin, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    org_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    worker_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    salary = db.Column(db.Integer)
    title = db.Column(db.String)
    resume = db.relationship("Resume", backref='vacancy')

    def __init__(self,
                 org_id=None,
                 worker_id=None,
                 salary=None,
                 title=None):
        super().__init__(org_id=org_id, worker_id=worker_id, salary=salary, title=title)

    @classmethod
    def new(cls, org_id, worker_id, salary, title):
        super().new(org_id, worker_id, salary, title)

    def has_permission(self, user):
        return self.organization.owner_id == user.id or user in self.organization.personnels


class Resume(db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vacancy_id = db.Column(db.Integer, db.ForeignKey('vacancy.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.String)
