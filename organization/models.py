from app import db, session
from datetime import datetime
from app.models import base_new
from users.models import User


class Organization(db.Model):
    __tablename__ = 'organizations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=True)
    creation_date = db.Column(db.Date, default=datetime.now)
    personnels = db.relationship("User", foreign_keys=[User.work_department_id], backref='binded_org', lazy='select')
    vacancies = db.relationship("Vacancy", backref='organization')
    owner_id = db.Column(db.Integer)
    org_type = db.Column(db.String)
    org_desc = db.Column(db.String)

    def __repr__(self):
        return f'<Organization {self.name}>'

    @classmethod
    def get_attached_to_personnel(cls, user):  # Возвращает организацию, к которой привязан кадровик
        return user.binded_org

    @classmethod
    def get_by_id(cls, user, org_id: int):
        org = session.query(cls).get(org_id)
        if user.id != org.owner_id:  # если пользователь ею не владеет
            return None
        return org

    @classmethod
    def get_attached_to_user(cls, user):  # Возвращает организации, которыми обладает пользователь
        return session.query(cls).filter(cls.owner_id == user.id).all()

    @classmethod
    def new(cls, name, owner_id, org_type, org_desc, date=datetime.now):
        kwargs = {"name": name, "owner_id": owner_id, "org_desc": org_desc, "org_type": org_type, "date": date}
        base_new(cls, **kwargs)

    def get_base_info(self):
        return self.id, self.name

    def get_full_info(self):
        return self.id, self.org_type, self.name, self.creation_date, self.org_desc, 'Путь к картинке'

    def get_required_workers(self):
        return [(vacancy.title, vacancy.salary) for vacancy in self.vacancies if vacancy.worker_id is None]

    def get_personnel(self):
        return [(hr.full_name, hr.salary, hr.id, bool(hr.t2_rel)) for hr in self.personnels]

    def get_workers(self):
        return [
            (vacancy.worker.full_name, vacancy.title, vacancy.salary, vacancy.worker.id, bool(vacancy.worker.t2_rel))
            for vacancy in self.vacancies if vacancy.worker_id is not None]


class Vacancy(db.Model):
    __tablename__ = 'vacancies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    org_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))
    worker_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    salary = db.Column(db.Integer)
    title = db.Column(db.String)

    @classmethod
    def new(cls, org_id, worker_id, salary, title):
        kwargs = {
            'org_id': org_id,
            'worker_id': worker_id,
            'salary': salary,
            'title': title,
        }
        base_new(cls, **kwargs)
