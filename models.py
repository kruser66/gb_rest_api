from peewee import *

db = MySQLDatabase(
	database='test',
	user='root',
	password='1234',
	host='127.0.0.1',
	port=3306)


class BaseModel(Model):
	class Meta:
		database = db


class Users(BaseModel):
	idAdmin = IntegerField()
	login = CharField()
	email = CharField()


class Persons(BaseModel):
	name = CharField()
	addedBy = IntegerField()
	
	
class Keywords(BaseModel):
	name = CharField()
	personID = IntegerField()


class Personspagerank(BaseModel):
	personID = IntegerField()
	pageID = IntegerField()
	rank = IntegerField()
	
	class Meta:
		primary_key = False

# if __name__ == '__main__':
# 	generate_users(10)
