from peewee import *

# import uuid

db = MySQLDatabase(
	database='test',
	user='root',
	password='1234',
	host='127.0.0.1',
	port=3306)


# def init_tables():
#     db.create_tables([Users], safe=True)
#
#
# def generate_users(num_users):
#     for i in range(num_users):
#         user_name = str(uuid.uuid4())[0:8]
#         Users(username=user_name).save()


class BaseModel(Model):
	class Meta:
		database = db


class Users(BaseModel):
	parentID = IntegerField()
	idAdmin = IntegerField()
	login = CharField()
	email = CharField()


class Persons(BaseModel):
	name = CharField()
	
	
class Keywords(BaseModel):
	name = CharField()
	personID = IntegerField()


# if __name__ == '__main__':
# 	generate_users(10)
