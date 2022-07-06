import sys, os, inspect
import mysql.connector
from mysql.connector import Error
import pandas as pd

sys.path.insert(0, (str(sys.path[0]))+"/../") 

from S3Connection import S3Connection
from DBConnection import DBConnection

BUCKET_NAME = "foxybyteswe"

def main():

	db = DBConnection()

	print("Creating connection to mysql server...")
	db.createServerConnection()

	print("Listing existing databases...")
	db.executeQuery("SHOW DATABASES;", db.server_connection);

	print("Creating connection to database 'Testing'...")
	db.createDatabaseConnection("Testing")

	print("Listing tables...")
	db.executeQuery("SHOW TABLES;");
	#insertRestaurants(connection)

	#uploadDB()
	#downloadDB()

if __name__ == "__main__":
	main()
