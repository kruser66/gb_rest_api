import falcon
from models import *
from playhouse.shortcuts import model_to_dict
import json

API_DESC = [
	{
		'api_url': '/v1/',
		'command': 'get',
		'comments': 'Описание доступных методов (этот документ)'
	},
	{
		'api_url': '/v1/users',
		'command': 'get',
		'comments': 'Получить список пользователей'
	},
	{
		'api_url': '/v1/users/{user_id}',
		'command': 'get',
		'comments': 'Получить пользователя user_id'
	},
	{
		'api_url': '/v1/persons',
		'command': 'get',
		'comments': 'Получить список персон'
	},
	{
		'api_url': '/v1/persons/{persons_id}',
		'command': 'get',
		'comments': 'Получить ключевые слова для person_id'
	},
	{
		'api_url': '/v1/persons/rank',
		'command': 'get',
		'comments': 'Получить список персон с их рангами по всем сайтам'
	},
]

json_params = {
	'ensure_ascii': False,
	'sort_keys': True,
	'indent': 4
}


class UserIdResource(object):
	def on_get(self, req, resp, user_id):
		try:
			user = Users.get(Users.id == user_id)
			resp.body = json.dumps(model_to_dict(user), **json_params)
			resp.status = falcon.HTTP_200
		except Exception as e:
			resp.body = json.dumps({'error': str(e)})
			resp.status = falcon.HTTP_500
			return resp


class UserResource:
	def on_get(self, req, resp):
		users = Users.select().order_by(Users.id)
		resp.body = json.dumps([model_to_dict(u) for u in users], **json_params)
		resp.status = falcon.HTTP_200


class PersonsResource(object):
	def on_get(self, req, resp):
		persons = Persons.select().order_by(Persons.id)
		resp.body = json.dumps([model_to_dict(u) for u in persons], **json_params)
		resp.status = falcon.HTTP_200


class KeywordsResource(object):
	def on_get(self, req, resp, person_id):
		person = Persons.get(Persons.id == person_id)
		output = model_to_dict(person)
		keywords = Keywords.select().where(Keywords.personID == person_id)
		output['keywords'] = [model_to_dict(u) for u in keywords]
		resp.body = json.dumps(output, **json_params)
		resp.status = falcon.HTTP_200


class Wiki(object):
	def on_get(self, req, resp):
		resp.body = json.dumps(API_DESC, **json_params)


class RankResource(object):
	def on_get(self, req, resp):
		ranks = Personspagerank.select().order_by(Personspagerank.personID)
		resp.body = json.dumps([model_to_dict(u) for u in ranks], **json_params)
		resp.status = falcon.HTTP_200


class RankIdResource(object):
	def on_get(self, req, resp, person_id):
		ranks = Personspagerank.select().where(Personspagerank.personID == person_id)
		resp.body = json.dumps([model_to_dict(u) for u in ranks], **json_params)
		resp.status = falcon.HTTP_200


class SiteResource(object):
	def on_get(self, req, resp):
		sites = Sites.select().order_by(Sites.id)
		resp.body = json.dumps([model_to_dict(u) for u in sites], **json_params)
		resp.status = falcon.HTTP_200


class SiteIdResource(object):
	def on_get(self, req, resp, site_id):
		sites = Sites.select().where(Sites.id == site_id)
		resp.body = json.dumps([model_to_dict(u) for u in sites], **json_params)
		resp.status = falcon.HTTP_200


api = falcon.API()

users = UserResource()
users_id = UserIdResource()
persons = PersonsResource()
keywords = KeywordsResource()
wiki = Wiki()
rank = RankResource()
rank_id = RankIdResource()
sites = SiteResource()
sites_id = SiteIdResource()

api.add_route('/v1/', wiki)
api.add_route('/v1/users', users)
api.add_route('/v1/users/{user_id}', users_id)
api.add_route('/v1/sites', sites)
api.add_route('/v1/sites/{site_id}', sites_id)
api.add_route('/v1/persons', persons)
api.add_route('/v1/persons/{person_id}', keywords)
api.add_route('/v1/persons/rank', rank)
api.add_route('/v1/persons/rank/{person_id}', rank_id)
