from flask import jsonify
import json
from flask_login import current_user
from flask_restful import reqparse, Resource
from app.api_utils import abort_obj_not_found
from app.tokens import check_tokens
from organization.models import Organization, Vacancy


def abort_org_not_found(org_id):
    abort_obj_not_found(org_id, Organization)


class OrganizationResource(Resource):
    def get(self, api_token, org_id):
        abort_org_not_found(org_id)
        org = Organization.get_by(id=org_id)
        if not check_tokens(org.api_token, api_token):
            return jsonify({'organization': 'Operation not allowed to this organization(incorrect token)'})
        return jsonify({'organization': org.to_dict(
            only=('id', 'name', 'creation_date', 'vacancies', 'owner_id', 'org_type', 'org_desc'))})

    def delete(self, api_token, org_id):
        abort_org_not_found(org_id)
        org = Organization.get_by(id=org_id)
        if not check_tokens(org.api_token, api_token):
            return jsonify({'deleting': 'Operation not allowed to this organization'})
        org.delete()
        return jsonify({'deleting': 'OK'})


class OrganizationListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True)
    parser.add_argument('org_type', required=True)
    parser.add_argument('org_desc', required=True)

    def get(self):
        orgs = Organization.all()
        return jsonify({'organization': [org.to_dict(
            only=('id', 'name', 'creation_date', 'vacancies', 'owner_id', 'org_type', 'org_desc')) for org
            in orgs]})

    def post(self):
        args = self.parser.parse_args()
        org = Organization.new(
            name=args['name'],
            owner_id=getattr(current_user, "id", None),
            org_type=args['org_type'],
            org_desc=args['org_desc']
        )
        org.save(add=True)
        return jsonify({'adding': 'OK'})


class VacancyListResource(Resource):
    def get(self):
        vacancies = [vac for vac in Vacancy.all() if vac.worker_id == None]
        # Выглядит ущербнее,но метод to_dict есть только у SerializerMixin,
        # а добавление его в родители Vacancy дает рекурсию при вызове организации
        return jsonify({'vacancy': [
            {'id': vac.id, 'org_id': vac.org_id, 'salary': vac.salary, 'title': vac.title} for
            vac in vacancies]})
