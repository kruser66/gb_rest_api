import falcon
from models import *
from playhouse.shortcuts import model_to_dict
import json
from datetime import datetime, timedelta

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
	{
		'api_url': '/v1/persons/rank/{person_id}',
		'command': 'get',
		'comments': 'Получить список рангов по всем сайтам для person_id'
	},
	{
		'api_url': '/v1/sites',
		'command': 'get',
		'comments': 'Получить список сайтов'
	},
	{
		'api_url': '/v1/sites/{site_id}',
		'command': 'get',
		'comments': 'Получить сайт по site_id'
	},
	{
		'api_url': '/v1/persons/rank/date?_from=YYYYMMDDDHHMMSS&_till=YYYYMMDDDHHMMSS',
		'command': 'get',
		'comments': 'Получить список персон с их рангами по всем сайтам за период _from _till'
	},
	{
		'api_url': '/v1/persons/rank/{person_id}/date?_from=YYYYMMDDDHHMMSS&_till=YYYYMMDDDHHMMSS',
		'command': 'get',
		'comments': 'Получить ранг {person_id} по всем сайтам за период _from _till'
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
			resp.body = json.dumps({'error': 'Неверный номер id'}, **json_params)
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
		try:
			person = Persons.get(Persons.id == person_id)
			output = model_to_dict(person)
			keywords = Keywords.select().where(Keywords.personID == person_id)
			output['keywords'] = [model_to_dict(u) for u in keywords]
			resp.body = json.dumps(output, **json_params)
			resp.status = falcon.HTTP_200
		except Exception as e:
			resp.body = json.dumps({'error': 'Неверный номер id'}, **json_params)
			resp.status = falcon.HTTP_500
			return resp


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
		try:
			sites = Sites.select().where(Sites.id == site_id)
			resp.body = json.dumps([model_to_dict(u) for u in sites], **json_params)
			resp.status = falcon.HTTP_200
		except Exception as e:
			resp.body = json.dumps({'error': 'Неверный номер id'}, **json_params)
			resp.status = falcon.HTTP_500
			return resp


class RankDateResource(object):
	def on_get(self, req, resp):
		if req.params:
			date_from = datetime.strptime(req.params['_from'], '%Y%m%d').date()
			date_till = datetime.strptime(req.params['_till'], '%Y%m%d').date()+timedelta(days=1)
			ranks = Personspagerank.select().join(Pages).where(
				Pages.lastScanDate.between(date_from, date_till))
			resp.body = json.dumps([model_to_dict(u) for u in ranks], **json_params)
			resp.status = falcon.HTTP_200
		else:
			output = [{'error': 'Недостаточно параметров'}, API_DESC[9]]
			resp.body = json.dumps(output, **json_params)
			resp.status = falcon.HTTP_500
			return resp


class RankDateIdResource(object):
	def on_get(self, req, resp, person_id):
		if req.params:
			date_from = datetime.strptime(req.params['_from'], '%Y%m%d').date()
			date_till = datetime.strptime(req.params['_till'], '%Y%m%d').date()+timedelta(days=1)
			ranks = Personspagerank.select().where(Personspagerank.personID == person_id)\
				.join(Pages).where(Pages.lastScanDate.between(date_from, date_till))
			resp.body = json.dumps([model_to_dict(u) for u in ranks], **json_params)
			resp.status = falcon.HTTP_200
		else:
			output = [{'error': 'Недостаточно параметров'}, API_DESC[10]]
			resp.body = json.dumps(output, **json_params)
			resp.status = falcon.HTTP_500
			return resp


api = falcon.API()

api.add_route('/v1/', Wiki())
api.add_route('/v1/users', UserResource())
api.add_route('/v1/users/{user_id}', UserIdResource())
api.add_route('/v1/sites', SiteResource())
api.add_route('/v1/sites/{site_id}', SiteIdResource())
api.add_route('/v1/persons', PersonsResource())
api.add_route('/v1/persons/{person_id}', KeywordsResource())
api.add_route('/v1/persons/rank', RankResource())
api.add_route('/v1/persons/rank/{person_id}', RankIdResource())
api.add_route('/v1/persons/rank/date', RankDateResource())
api.add_route('/v1/persons/rank/{person_id}/date', RankDateIdResource())
