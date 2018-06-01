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
	isAdmin = IntegerField()
	login = CharField()
	email = CharField()


class Sites(BaseModel):
	name = CharField()
	addedBy = IntegerField()
	siteDescription = CharField()


class Pages(BaseModel):
	url = CharField()
	siteId = ForeignKeyField(Sites, column_name='siteID', to_field='id')
	foundDateTime = CharField()
	lastScanDate = CharField()


class Persons(BaseModel):
	name = CharField()
	addedBy = IntegerField()


class Personspagerank(BaseModel):
	personID = ForeignKeyField(Persons, column_name='personID', to_field='id')
	pageID = ForeignKeyField(Pages, column_name='pageID', to_field='id')
	rank = IntegerField()
	
	class Meta:
		primary_key = False


class Keywords(BaseModel):
	name = CharField()
	personID = IntegerField()




	
	




