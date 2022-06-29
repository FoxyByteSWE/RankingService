import sys, os
import mysql.connector
from mysql.connector import Error
import pandas as pd

from s3 import uploadFile, downloadFile, deleteFile

from database import create_server_connection, create_database, create_db_connection, execute_query

BUCKET_NAME = "foxybyteswe"

def main():
	print("Creating connection to mysql service...")
	connection = create_server_connection("localhost", "root", "root")

	print("Listing existing databases...")

	print("Creating connection to database \Testing'...")
	create_database(connection, "CREATE DATABASE IF NOT EXISTS Testing")

	connection = create_db_connection("localhost", "root", "root", "Testing")
	execute_query(connection, "show tables;");

	#connection = create_db_connection("localhost", "root", "root", "Testing")
	#insertRestaurants(connection)

	#uploadDB()
	#downloadDB()

if __name__ == "__main__":
	main()
