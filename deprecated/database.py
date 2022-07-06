# standard packages
import sys, os
import mysql.connector
from mysql.connector import Error
import pandas as pd

# packages written as part of the project
from analyzer import rank
from S3Connection import S3Connection
from restaurant import Restaurant, Media, json2Restaurants

# S3 bucket name
BUCKET_NAME = "foxybyteswe"

##### Functions
def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Success")
    except Error as err:
        print(f"Error: '{err}'")

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

def insertRestaurants(connection):
	execute_query(connection, drop_restaurants)
	execute_query(connection, create_restaurants)
	restaurants = json2Restaurants((str(sys.path[0]))+"/../IGCrawlerService/crawler/data/locationsData.json")
	for r in restaurants:
		r.assignValues()
	rank(restaurants)
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
		print(address)
		if address == '""' or address == '"None", ':
			address = 'NULL, '
		website = '"' + str(r.website) + '", '
		if website == '""' or website == '"None", ':
			website = 'NULL, '
		phone = '"' + str(r.phone) + '", '
		if phone == '""' or phone == '"None", ':
			phone = 'NULL, '
		lng = '"' + str(r.coordinates[0]) + '", '
		if lng == '""' or lng == '"None", ':
			lng = 'NULL, '
		lat = '"' + str(r.coordinates[1]) + '", '
		if lat == '""' or lat == '"None", ':
			lat = 'NULL, '
		ranking = '"' + str(r.returnFormattedRanking()) + '"'
		if ranking == '""' or ranking == '"None", ':
			ranking = 'NULL, '
		query = insert_restaurant + pk + name + category + address + website + phone + lng + lat + ranking + ');'
		print(query)
		execute_query(connection, query)

def uploadDB():
	os.system('mysqldump -u "root" -p "Restaurants" > Restaurants.sql')
	s3 = S3Connection(BUCKET_NAME)
	s3.uploadFile((str(sys.path[0]))+"/Restaurants.sql")

def downloadDB():
	s3 = S3Connection(BUCKET_NAME)
	s3.downloadFile("Restaurants.sql", (str(sys.path[0]))+"/Restaurants.sql")
	connection = create_server_connection("localhost", "root", "root")
	execute_query(connection, "DROP DATABASE IF EXISTS Restaurants")
	create_database(connection, "CREATE DATABASE IF NOT EXISTS Restaurants")
	os.system('mysql -u root -p Restaurants < Restaurants.sql')

##### Queries
drop_restaurants = "DROP TABLE IF EXISTS Restaurants"
create_restaurants = """CREATE TABLE IF NOT EXISTS Restaurants(
	Codice_pk VARCHAR(20) PRIMARY KEY,
	Nome VARCHAR(50) NOT NULL,
	Categoria  VARCHAR(20),
	Indirizzo VARCHAR(100),
	Sito VARCHAR(70),
	Telefono VARCHAR(16),
	Longitudine FLOAT,
	Latitudine FLOAT,
	Ranking FLOAT
)"""

insert_restaurant = "INSERT INTO Restaurants VALUES ("

##### Main
def main():
	connection = create_server_connection("localhost", "root", "root")
	create_database(connection, "CREATE DATABASE IF NOT EXISTS Restaurants")

	connection = create_db_connection("localhost", "root", "root", "Restaurants")
	insertRestaurants(connection)

	uploadDB()
	downloadDB()

if __name__ == "__main__":
	main()
