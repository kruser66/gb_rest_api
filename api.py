import falcon
from models import *
from playhouse.shortcuts import model_to_dict
import json

API_DESC = [
	{
		'api_url': '/v1/',
		'command': 'get',
		'comments': 'Описание доступных методов'
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
]


class UserIdResource(object):
	def on_get(self, req, resp, user_id):
		try:
			user = Users.get_or_none(Users.id == user_id)
			resp.body = json.dumps(model_to_dict(user), ensure_ascii=False)
			resp.status = falcon.HTTP_200
		except Exception as e:
			resp.body = json.dumps({'error': str(e)})
			resp.status = falcon.HTTP_500
			return resp


class UserResource:
	def on_get(self, req, resp):
		users = Users.select().order_by(Users.id)
		resp.body = json.dumps([model_to_dict(u) for u in users], ensure_ascii=False)
		resp.status = falcon.HTTP_200


class PersonsResource(object):
	def on_get(self, req, resp):
		persons = Persons.select().order_by(Persons.id)
		resp.body = json.dumps([model_to_dict(u) for u in persons], ensure_ascii=False)
		resp.status = falcon.HTTP_200


class KeywordsResource(object):
	def on_get(self, req, resp, person_id):
		keywords = Keywords.select().where(Keywords.personID == person_id)
		resp.body = json.dumps([model_to_dict(u) for u in keywords], ensure_ascii=False)
		resp.status = falcon.HTTP_200


class Wiki(object):
	def on_get(self, req, resp):
		resp.body = json.dumps(API_DESC, ensure_ascii=False)


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