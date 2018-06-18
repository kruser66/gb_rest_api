import falcon
from models import *
from playhouse.shortcuts import model_to_dict
import json
from datetime import datetime, timedelta
import uuid


EXPIRED_TIME = 3
API_DESC = [
	{
		'api_url': '/v1/',
		'command': 'get',
		'comments': 'Описание доступных методов (этот документ)'
	},
	{
		'api_url': '/v1/auth',
		'command': 'post',
		'comments': 'Получить токен для пользователя',
		'content': "Content-Type: application/json",
		'data': {"user": "some_user", "password": "correct_pass"}
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


def datetime_handler(x):
	if isinstance(x, datetime):
		return x.strftime('%Y-%m-%d %H:%M:%S')


json_params = {
	'ensure_ascii': False,
	'indent': 4,
	'default': datetime_handler
}

exclude = [Users.password, Users.token, Users.tokencreateddate, Users.tokenlastaccess]


def check_auth_token():
	pass


class UserIdResource(object):
	def on_get(self, req, resp, user_id):
		try:
			user = Users.get(Users.id == user_id)
			resp.body = json.dumps(model_to_dict(user, exclude=exclude), **json_params)
			resp.status = falcon.HTTP_200
		except Exception as e:
			resp.body = json.dumps({'error': 'Неверный номер id'}, **json_params)
			resp.status = falcon.HTTP_500
			return resp


class UserResource:
	def on_get(self, req, resp):
		users = Users.select().order_by(Users.id)
		resp.body = json.dumps([model_to_dict(u, exclude=exclude, recurse=False) for u in users], **json_params)
		resp.status = falcon.HTTP_200


class AuthResource(object):
	def on_get(self, req, resp):
		resp.status = falcon.HTTP_404
	
	def on_post(self, req, resp):
		body = json.loads(req.stream.read().decode('utf-8'))
		try:
			user = Users.get_or_none(Users.login == body['user'])
			if user and user.password == body['password']:
				if (user.token is None) or ((user.tokencreateddate + timedelta(minutes=EXPIRED_TIME)) < datetime.now()):
					new_token = uuid.uuid4()
					user.token = new_token
					user.tokencreateddate = datetime.now()
					user.tokenlastaccess = datetime.now()
					user.save()
					user = Users.get(Users.login == body['user'])
				output = {'success': '1', 'token': user.token, 'user_id': user.id}
			else:
				output = {'success': '0'}
			resp.body = json.dumps(output, **json_params)
			resp.status = falcon.HTTP_200
		except:
			resp.body = json.dumps({'success': '0'}, **json_params)
			resp.body = falcon.HTTP_500


class PersonsResource(object):
	def on_get(self, req, resp):
		persons = Persons.select().order_by(Persons.id)
		resp.body = json.dumps([model_to_dict(u, exclude=exclude, recurse=False) for u in persons], **json_params)
		resp.status = falcon.HTTP_200


class KeywordsResource(object):
	def on_get(self, req, resp, person_id):
		try:
			person = Persons.get(Persons.id == person_id)
			output = model_to_dict(person, exclude=exclude, recurse=False)
			keywords = Keywords.select().where(Keywords.personid == person_id)
			output['keywords'] = [model_to_dict(u, exclude=exclude, recurse=False) for u in keywords]
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
		ranks = Personspagerank.select().order_by(Personspagerank.personid)
		resp.body = json.dumps([model_to_dict(u, exclude=exclude, recurse=False) for u in ranks], **json_params)
		resp.status = falcon.HTTP_200


class RankIdResource(object):
	def on_get(self, req, resp, person_id):
		ranks = Personspagerank.select().where(Personspagerank.personid == person_id)
		resp.body = json.dumps([model_to_dict(u, exclude=exclude, recurse=False) for u in ranks], **json_params)
		resp.status = falcon.HTTP_200


class SiteResource(object):
	def on_get(self, req, resp):
		sites = Sites.select().order_by(Sites.id)
		resp.body = json.dumps([model_to_dict(u, exclude=exclude) for u in sites], **json_params)
		resp.status = falcon.HTTP_200


class SiteIdResource(object):
	def on_get(self, req, resp, site_id):
		try:
			sites = Sites.select().where(Sites.id == site_id)
			resp.body = json.dumps([model_to_dict(u, exclude=exclude) for u in sites], **json_params)
			resp.status = falcon.HTTP_200
		except Exception as e:
			resp.body = json.dumps({'error': 'Неверный номер id'}, **json_params)
			resp.status = falcon.HTTP_500
			return resp


class RankDateResource(object):
	def on_get(self, req, resp):
		if req.params:
			date_from = datetime.strptime(req.params['_from'], '%Y%m%d%H%M%S')
			date_till = datetime.strptime(req.params['_till'], '%Y%m%d%H%M%S')
			ranks = Personspagerank.select().join(Pages).where(
				Pages.lastscandate.between(date_from, date_till))
			resp.body = json.dumps([model_to_dict(u, exclude=exclude, recurse=False) for u in ranks], **json_params)
			resp.status = falcon.HTTP_200
		else:
			output = [{'error': 'Недостаточно параметров'}, API_DESC[10]]
			resp.body = json.dumps(output, **json_params)
			resp.status = falcon.HTTP_500
			return resp


class RankDateIdResource(object):
	def on_get(self, req, resp, person_id):
		if req.params:
			try:
				date_from = datetime.strptime(req.params['_from'], '%Y%m%d%H%M%S')  # .date()
				date_till = datetime.strptime(req.params['_till'], '%Y%m%d%H%M%S')  # .date()+timedelta(days=1)
				ranks = Personspagerank.select().where(Personspagerank.personid == person_id) \
					.join(Pages).where(Pages.lastscandate.between(date_from, date_till))
				resp.body = json.dumps([model_to_dict(u, exclude=exclude, recurse=False) for u in ranks], **json_params)
				resp.status = falcon.HTTP_200
			except:
				output = [{'error': 'Недостаточно параметров'}, API_DESC[11]]
				resp.body = json.dumps(output, **json_params)
				resp.status = falcon.HTTP_500
			return resp


class PeeweeConnectionMiddleware(object):
	def process_request(self, req, resp):
		database.connect()
	
	def process_response(self, req, resp, resource):
		if not database.is_closed():
			database.close()


api = falcon.API(middleware=[
	PeeweeConnectionMiddleware(),
])

api.add_route('/v1/', Wiki())
api.add_route('/v1/auth', AuthResource())
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
