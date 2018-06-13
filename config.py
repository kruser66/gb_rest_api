from peewee import *

database = MySQLDatabase(
	database='searchandratewords',
	user='root',
	password='1234',
	host='127.0.0.1',
	port=3306)
