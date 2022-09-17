import logging
import pymysql

from Media import Media
from Restaurant import Restaurant

class DBConnection:

	def __init__(self, hostname = "michelinsocial.ctr0m4f2rgau.eu-west-1.rds.amazonaws.com", user = "admin", password = "#g7ct=MD", server_connection = None, database_connection = None):
		self.hostname = hostname
		self.user = user
		self.password = password
		self.server_connection = server_connection
		self.database_connection = database_connection

	def createServerConnection(self, host_name = None, user_name = None, user_password = None):

		if host_name is None:
			host_name = self.hostname

		if user_name is None:
			user_name = self.user

		if user_password is None:
			user_password = self.password

		connection = None
		try:
			connection = pymysql.connect(
				host = host_name,
				user = user_name,
				passwd = user_password
			)
			print("Successfully connected to MySQL server")
		except pymysql.Error as err:
			print(f"Error: '{err}'")

		self.server_connection = connection
		return connection

	def createDatabase(self, name, connection = None):

		if connection is None:
			connection = self.server_connection

		cursor = connection.cursor()

		"""
		query = "DROP DATABASE IF EXISTS " + name + ";"
		try:
			cursor.execute(query)
			print("Successfully dropped database " + name)
		except Error as err:
			print(f"Error: '{err}'")
		"""

		query = "CREATE DATABASE IF NOT EXISTS " + name + ";"
		try:
			cursor.execute(query)
			connection.commit()
			print("Successfully created database " + name)
		except pymysql.Error as err:
			print(f"Error: '{err}'")

	def createDatabaseConnection(self, db_name, host_name = None, user_name = None, user_password = None):

		if host_name is None:
			host_name = self.hostname

		if user_name is None:
			user_name = self.user

		if user_password is None:
			user_password = self.password

		connection = None
		try:
			connection = pymysql.connect(
				host = host_name,
				user = user_name,
				passwd = user_password,
				database = db_name
			)
			print("Successfully connected to database " + db_name)
		except pymysql.Error as err:
			print(f"Error: '{err}'")

		self.database_connection = connection
		return connection

	def executeQuery(self, query, connection = None):

		if connection is None:
			connection = self.database_connection

		cursor = connection.cursor()
		try:
			cursor.execute(query)
			connection.commit()
			print("Successfully executed " + query)
			print("\nResult:")
			result = cursor.fetchall();
			for row in result:
				print(row)
		except pymysql.Error as err:
			print(f"Error: '{err}'")

	def insertRestaurants(self, restaurants, connection = None):

		if connection is None:
			connection = self.database_connection

		drop_restaurants = "DROP TABLE IF EXISTS restaurants;"

		create_restaurants = """CREATE TABLE IF NOT EXISTS restaurants(
			Codice_pk VARCHAR(20) PRIMARY KEY,
			Nome VARCHAR(50) NOT NULL,
			Categoria  VARCHAR(20),
			Indirizzo VARCHAR(150),
			Sito VARCHAR(70),
			Telefono VARCHAR(16),
			Immagine VARCHAR(1500),
			Longitudine FLOAT,
			Latitudine FLOAT,
			Ranking FLOAT,
			Commento_1_URL VARCHAR(1500),
			Commento_1_testo VARCHAR(1000),
			Commento_2_URL VARCHAR(1500),
			Commento_2_testo VARCHAR(1000)
		)"""

		self.executeQuery(drop_restaurants)

		self.executeQuery(create_restaurants)

		for r in restaurants:
			#print(r.pk)
			#print(r.name)
			#r.printRanking()
			#print('\n')
			pk = '"' + str(r.pk) + '", '
			if pk == '""' or pk == '"None", ':
				pk = 'NULL, '
			name = str(r.name)
			name = name.replace('"', "'")
			name = '"' + name + '", '
			if name == '""' or name == '"None", ':
				name = 'NULL, '
			category = '"' + str(r.category) + '", '
			if category == '""' or category == '"None", ':
				category = 'NULL, '
			address = '"' + str(r.address) + '", '
			#print(address)
			if address == '""' or address == '"None", ':
				address = 'NULL, '
			website = '"' + str(r.website) + '", '
			if website == '""' or website == '"None", ':
				website = 'NULL, '
			phone = '"' + str(r.phone) + '", '
			if phone == '""' or phone == '"None", ':
				phone = 'NULL, '
			main_image_url = '"' + str(r.main_image_url) + '", '
			if main_image_url == '""' or main_image_url == '"None", ':
				main_image_url = 'NULL, '
			lng = '"' + str(r.coordinates[0]) + '", '
			if lng == '""' or lng == '"None", ':
				lng = 'NULL, '
			lat = '"' + str(r.coordinates[1]) + '", '
			if lat == '""' or lat == '"None", ':
				lat = 'NULL, '
			ranking = '"' + str(r.returnFormattedRanking()) + '", '
			if ranking == '""' or ranking == '"None", ':
				ranking = 'NULL, '

			if len(r.comments) > 0:
				comment_1_url = '"' + str(r.comments[0][0]) + '", '
				if comment_1_url == '""' or comment_1_url == '"None", ':
					comment_1_url = 'NULL, '
				comment_1_text = '"' + str(r.comments[0][1]) + '", '
				if comment_1_text == '""' or comment_1_text == '"None", ':
					comment_1_text = 'NULL, '
			else:
				comment_1_url = 'NULL, '
				comment_1_text = 'NULL, '
			if len(r.comments) > 1:
				comment_2_url = '"' + str(r.comments[1][0]) + '", '
				if comment_2_url == '""' or comment_2_url == '"None", ':
					comment_2_url = 'NULL, '
				comment_2_text = '"' + str(r.comments[1][1]) + '", '
				if comment_2_text == '""' or comment_2_text == '"None", ':
					comment_2_text = 'NULL, '
			else:
				comment_2_url = 'NULL, '
				comment_2_text = 'NULL '

			insert_restaurant = "INSERT INTO restaurants VALUES (" + pk + name + category + address + website + phone + main_image_url + lng + lat + ranking + comment_1_url + comment_1_text + comment_2_url + comment_2_text + ');'
			#print(insert_restaurant)
			self.executeQuery(insert_restaurant)
