from peewee import *
from config import database


class BaseModel(Model):
	class Meta:
		database = database


class Users(BaseModel):
	id = AutoField(column_name='ID')
	email = CharField()
	isadmin = IntegerField(column_name='isAdmin')
	login = CharField()
	parentid = ForeignKeyField(column_name='parentID', field='id', model='self', null=True)
	password = CharField()
	token = CharField(null=True, unique=True)
	tokencreateddate = DateTimeField(column_name='tokenCreatedDate', null=True)
	tokenlastaccess = DateTimeField(column_name='tokenLastAccess', formats=['%Y-%m-%d %H:%M:%S'], null=True)
	
	class Meta:
		table_name = 'users'


class Persons(BaseModel):
	id = AutoField(column_name='ID')
	addedby = ForeignKeyField(column_name='addedBy', field='id', model=Users)
	name = CharField()
	
	class Meta:
		table_name = 'persons'


class Keywords(BaseModel):
	id = AutoField(column_name='ID')
	name = CharField()
	personid = ForeignKeyField(column_name='personID', field='id', model=Persons)
	
	class Meta:
		table_name = 'keywords'


class Log(BaseModel):
	id = AutoField(column_name='ID')
	action = CharField()
	adminid = ForeignKeyField(column_name='adminID', field='id', model=Users)
	logdate = DateTimeField(column_name='logDate', constraints=[SQL("DEFAULT current_timestamp()")])
	
	class Meta:
		table_name = 'log'


class Sites(BaseModel):
	id = AutoField(column_name='ID')
	addedby = ForeignKeyField(column_name='addedBy', field='id', model=Users)
	name = CharField()
	sitedescription = CharField(column_name='siteDescription', null=True)
	
	class Meta:
		table_name = 'sites'


class Pages(BaseModel):
	id = AutoField(column_name='ID')
	url = CharField(column_name='URL')
	founddatetime = DateTimeField(column_name='foundDateTime')
	lastscandate = DateTimeField(column_name='lastScanDate', null=True)
	siteid = ForeignKeyField(column_name='siteID', field='id', model=Sites)
	
	class Meta:
		table_name = 'pages'


class Personspagerank(BaseModel):
	id = AutoField(column_name='ID')
	pageid = ForeignKeyField(column_name='PageID', field='id', model=Pages)
	personid = ForeignKeyField(column_name='PersonID', field='id', model=Persons)
	rank = IntegerField(column_name='Rank', null=True)
	
	class Meta:
		table_name = 'personspagerank'


