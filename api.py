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
		keywords = Keywords.select().where(Keywords.personID == person_id)
		resp.body = json.dumps([model_to_dict(u) for u in keywords], **json_params)
		resp.status = falcon.HTTP_200


class Wiki(object):
	def on_get(self, req, resp):
		resp.body = json.dumps(API_DESC, **json_params)


api = falcon.API()

users = UserResource()
users_id = UserIdResource()
persons = PersonsResource()
keywords = KeywordsResource()
wiki = Wiki()

api.add_route('/v1/', wiki)
api.add_route('/v1/users', users)
api.add_route('/v1/users/{user_id}', users_id)
api.add_route('/v1/persons', persons)
api.add_route('/v1/persons/{person_id}', keywords)